import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from core.permissions import PapelRequiredMixin
from .models import LancamentoFinanceiro, ContaFinanceira, ContaPagarReceber, RepasseMotorista, ComissaoOperacional, ConciliacaoBancaria, FechamentoFinanceiro
from .services import FinanceiroService
from core.forms import LancamentoFinanceiroForm

class FinanceiroDashboardView(LoginRequiredMixin, TemplateView):
    template_name='financeiro/dashboard.html'
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)
        ctx['dre']=FinanceiroService.calcular_dre(self.request.GET.get('inicio'), self.request.GET.get('fim'))
        ctx['contas_abertas']=ContaPagarReceber.objects.exclude(status__in=['BAIXADA','CANCELADA']).order_by('vencimento')[:10]
        ctx['repasses_pendentes']=RepasseMotorista.objects.exclude(status='PAGO').order_by('data_programada','id')[:10]
        ctx['comissoes_pendentes']=ComissaoOperacional.objects.exclude(status='PAGA').order_by('-criado_em')[:10]
        return ctx

class LancamentoFinanceiroListView(LoginRequiredMixin, ListView):
    model=LancamentoFinanceiro; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=20
    def get_queryset(self):
        qs=super().get_queryset().order_by('-id')
        q=self.request.GET.get('q')
        if q: qs=qs.filter(descricao__icontains=q)
        return qs
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Lançamentos financeiros','base_url':'financeiro','create_url':'financeiro:create'}); return ctx
class LancamentoFinanceiroDetailView(LoginRequiredMixin, DetailView): model=LancamentoFinanceiro; template_name='crud/detail.html'; context_object_name='objeto'
class LancamentoFinanceiroCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=LancamentoFinanceiro; form_class=LancamentoFinanceiroForm; template_name='crud/form.html'; success_url=reverse_lazy('financeiro:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Novo lançamento'; return ctx
class LancamentoFinanceiroUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=LancamentoFinanceiro; form_class=LancamentoFinanceiroForm; template_name='crud/form.html'; success_url=reverse_lazy('financeiro:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Editar lançamento'; return ctx
class LancamentoFinanceiroDeleteView(LoginRequiredMixin, PapelRequiredMixin, DeleteView):
    papeis_permitidos=['ADMIN']; model=LancamentoFinanceiro; template_name='crud/confirm_delete.html'; success_url=reverse_lazy('financeiro:list')

class ContaPagarReceberListView(LoginRequiredMixin, ListView):
    model=ContaPagarReceber; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=30
    def get_queryset(self):
        qs=super().get_queryset().select_related('frete','conta').order_by('vencimento')
        natureza=self.request.GET.get('natureza'); status=self.request.GET.get('status')
        if natureza: qs=qs.filter(natureza=natureza)
        if status: qs=qs.filter(status=status)
        return qs
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Contas a pagar e receber','base_url':'financeiro:contas'}); return ctx

class RepasseMotoristaListView(LoginRequiredMixin, ListView):
    model=RepasseMotorista; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=30
    def get_queryset(self): return super().get_queryset().select_related('frete','motorista').order_by('status','data_programada','id')
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Repasses de motoristas','base_url':'financeiro:repasses'}); return ctx

class ComissaoOperacionalListView(LoginRequiredMixin, ListView):
    model=ComissaoOperacional; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=30
    def get_queryset(self): return super().get_queryset().select_related('frete','usuario').order_by('status','-criado_em')
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Comissões operacionais','base_url':'financeiro:comissoes'}); return ctx

class ConciliacaoBancariaListView(LoginRequiredMixin, ListView):
    model=ConciliacaoBancaria; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=30
    def get_queryset(self): return super().get_queryset().select_related('conta','lancamento').order_by('-data_movimento')
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Conciliação bancária','base_url':'financeiro:conciliacao'}); return ctx

def dre_csv(request):
    dre=FinanceiroService.calcular_dre(request.GET.get('inicio'), request.GET.get('fim'))
    response=HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="dre_fusion_cargas.csv"'
    writer=csv.writer(response); writer.writerow(['Indicador','Valor'])
    for k,v in dre.items(): writer.writerow([k, v])
    return response

def contas_csv(request):
    response=HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="contas_pagar_receber.csv"'
    writer=csv.writer(response); writer.writerow(['Natureza','Descrição','Favorecido','Valor original','Valor pago','Saldo','Vencimento','Status'])
    for c in ContaPagarReceber.objects.all().order_by('vencimento'):
        writer.writerow([c.natureza,c.descricao,c.favorecido,c.valor_original,c.valor_pago,c.saldo,c.vencimento,c.status])
    return response
