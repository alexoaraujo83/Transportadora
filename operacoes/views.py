from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from fretes.models import Frete
from .models import ChecklistOperacional, ConsultaRisco, DocumentoFrete, OcorrenciaOperacional, TarefaOperacional
from .forms import ChecklistOperacionalForm, ConsultaRiscoForm, DocumentoFreteForm, OcorrenciaOperacionalForm, TarefaOperacionalForm
from .services import FluxoFreteService, RiscoService

@login_required
def kanban_fretes(request):
    status_list = [s[0] for s in Frete.Status.choices]
    colunas = {status: Frete.objects.filter(status=status).select_related('motorista','transportadora').order_by('-atualizado_em')[:50] for status in status_list}
    abertas = OcorrenciaOperacional.objects.exclude(status__in=['RESOLVIDA','CANCELADA']).count()
    tarefas_pendentes = TarefaOperacional.objects.filter(concluida=False).count()
    documentos_pendentes = DocumentoFrete.objects.filter(validado=False).count()
    return render(request, 'operacoes/kanban.html', {'colunas': colunas, 'status_labels': dict(Frete.Status.choices), 'abertas': abertas, 'tarefas_pendentes': tarefas_pendentes, 'documentos_pendentes': documentos_pendentes})

@login_required
def checklist_frete(request, pk):
    frete = get_object_or_404(Frete, pk=pk)
    checklist, _ = ChecklistOperacional.objects.get_or_create(frete=frete)
    if request.method == 'POST':
        form = ChecklistOperacionalForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save(); messages.success(request, 'Checklist atualizado.'); return redirect('operacoes:checklist', pk=frete.pk)
    else:
        form = ChecklistOperacionalForm(instance=checklist)
    return render(request, 'operacoes/checklist.html', {'frete': frete, 'form': form, 'checklist': checklist})

@login_required
def acao_status(request, pk, acao):
    frete = get_object_or_404(Frete, pk=pk)
    mapa = {'prospectar': Frete.Status.PROSPECTANDO, 'agendar': Frete.Status.AGENDADO, 'coleta': Frete.Status.EM_TRANSITO, 'entregar': Frete.Status.ENTREGUE, 'cancelar': Frete.Status.CANCELADO}
    if acao == 'coleta': FluxoFreteService.registrar_coleta(frete, request.user)
    elif acao == 'entregar': FluxoFreteService.registrar_descarga(frete, request.user)
    elif acao in mapa: FluxoFreteService.alterar_status(frete, mapa[acao], request.user, f'Ação operacional: {acao}')
    messages.success(request, 'Status atualizado com sucesso.')
    return redirect('operacoes:kanban')

@login_required
def consultas_risco(request):
    if request.method == 'POST':
        form = ConsultaRiscoForm(request.POST)
        if form.is_valid():
            consulta = form.save(); messages.success(request, f'Consulta registrada: {consulta.status}'); return redirect('operacoes:risco')
    else:
        form = ConsultaRiscoForm()
    consultas = ConsultaRisco.objects.select_related('motorista','frete').order_by('-criado_em')[:100]
    return render(request, 'operacoes/risco.html', {'form': form, 'consultas': consultas})

@login_required
def consultar_risco_motorista(request, motorista_id, frete_id=None):
    from motoristas.models import Motorista
    motorista = get_object_or_404(Motorista, pk=motorista_id)
    frete = get_object_or_404(Frete, pk=frete_id) if frete_id else None
    consulta = RiscoService.consultar_motorista(motorista, frete)
    messages.success(request, f'Consulta de risco gerada: {consulta.status}')
    return redirect('operacoes:risco')

class BaseOpList(LoginRequiredMixin, ListView):
    paginate_by = 25
    template_name = 'crud/list.html'

class BaseOpCreate(LoginRequiredMixin, CreateView):
    template_name='crud/form.html'

class BaseOpUpdate(LoginRequiredMixin, UpdateView):
    template_name='crud/form.html'

class BaseOpDelete(LoginRequiredMixin, DeleteView):
    template_name='crud/confirm_delete.html'
    success_url=reverse_lazy('operacoes:kanban')

class DocumentoListView(BaseOpList):
    model=DocumentoFrete
    fields=['frete','tipo','numero','validado']
    extra_context={'title':'Documentos de frete','create_url':'operacoes:documento_create'}
class DocumentoCreateView(BaseOpCreate):
    model=DocumentoFrete; form_class=DocumentoFreteForm; success_url=reverse_lazy('operacoes:documentos'); extra_context={'title':'Novo documento'}
class DocumentoUpdateView(BaseOpUpdate):
    model=DocumentoFrete; form_class=DocumentoFreteForm; success_url=reverse_lazy('operacoes:documentos'); extra_context={'title':'Editar documento'}
class DocumentoDeleteView(BaseOpDelete):
    model=DocumentoFrete

class OcorrenciaListView(BaseOpList):
    model=OcorrenciaOperacional
    fields=['frete','titulo','gravidade','status','responsavel']
    extra_context={'title':'Ocorrências operacionais','create_url':'operacoes:ocorrencia_create'}
class OcorrenciaCreateView(BaseOpCreate):
    model=OcorrenciaOperacional; form_class=OcorrenciaOperacionalForm; success_url=reverse_lazy('operacoes:ocorrencias'); extra_context={'title':'Nova ocorrência'}
class OcorrenciaUpdateView(BaseOpUpdate):
    model=OcorrenciaOperacional; form_class=OcorrenciaOperacionalForm; success_url=reverse_lazy('operacoes:ocorrencias'); extra_context={'title':'Editar ocorrência'}
class OcorrenciaDeleteView(BaseOpDelete):
    model=OcorrenciaOperacional

class TarefaListView(BaseOpList):
    model=TarefaOperacional
    fields=['frete','titulo','prazo','concluida','responsavel']
    extra_context={'title':'Tarefas operacionais','create_url':'operacoes:tarefa_create'}
class TarefaCreateView(BaseOpCreate):
    model=TarefaOperacional; form_class=TarefaOperacionalForm; success_url=reverse_lazy('operacoes:tarefas'); extra_context={'title':'Nova tarefa'}
class TarefaUpdateView(BaseOpUpdate):
    model=TarefaOperacional; form_class=TarefaOperacionalForm; success_url=reverse_lazy('operacoes:tarefas'); extra_context={'title':'Editar tarefa'}
class TarefaDeleteView(BaseOpDelete):
    model=TarefaOperacional
