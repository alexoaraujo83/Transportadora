from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from core.permissions import PapelRequiredMixin
from fretes.models import Frete
from .models import EventoRastreamento, PontoRota, PosicaoAtualFrete
from .services import MapasService, RastreamentoService
from core.forms import EventoRastreamentoForm, PontoRotaForm

class EventoRastreamentoListView(LoginRequiredMixin, ListView):
    model=EventoRastreamento; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=20
    def get_queryset(self):
        qs=super().get_queryset().select_related('frete').order_by('-criado_em')
        q=self.request.GET.get('q')
        if q: qs=qs.filter(descricao__icontains=q)
        return qs
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Rastreamento','base_url':'rastreamento','create_url':'rastreamento:create'}); return ctx
class EventoRastreamentoDetailView(LoginRequiredMixin, DetailView): model=EventoRastreamento; template_name='crud/detail.html'; context_object_name='objeto'
class EventoRastreamentoCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=EventoRastreamento; form_class=EventoRastreamentoForm; template_name='crud/form.html'; success_url=reverse_lazy('rastreamento:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Novo evento de rastreamento'; return ctx
class EventoRastreamentoUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=EventoRastreamento; form_class=EventoRastreamentoForm; template_name='crud/form.html'; success_url=reverse_lazy('rastreamento:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Editar rastreamento'; return ctx
class EventoRastreamentoDeleteView(LoginRequiredMixin, PapelRequiredMixin, DeleteView):
    papeis_permitidos=['ADMIN']; model=EventoRastreamento; template_name='crud/confirm_delete.html'; success_url=reverse_lazy('rastreamento:list')

class MapaFretesView(LoginRequiredMixin, TemplateView):
    template_name='rastreamento/mapa.html'
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)
        posicoes=PosicaoAtualFrete.objects.select_related('frete').all().order_by('-atualizado_em')
        ctx['posicoes']=posicoes
        ctx['titulo']='Mapa operacional de fretes'
        return ctx

class RotaFreteView(LoginRequiredMixin, TemplateView):
    template_name='rastreamento/rota.html'
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs)
        frete=get_object_or_404(Frete, pk=kwargs['frete_id'])
        pontos=PontoRota.objects.filter(frete=frete).order_by('sequencia')
        eventos=EventoRastreamento.objects.filter(frete=frete).order_by('-criado_em')[:30]
        ctx.update({'frete':frete,'pontos':pontos,'eventos':eventos,'percentual':RastreamentoService.calcular_percentual_rota(frete),'link_rota':MapasService.gerar_link_rota(pontos)})
        return ctx

class PontoRotaCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=PontoRota; form_class=PontoRotaForm; template_name='crud/form.html'
    def get_success_url(self): return reverse_lazy('rastreamento:rota', kwargs={'frete_id': self.object.frete_id})
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Novo ponto da rota'; return ctx

def concluir_ponto(request, pk):
    ponto=get_object_or_404(PontoRota, pk=pk)
    RastreamentoService.concluir_ponto(ponto)
    messages.success(request, 'Ponto da rota concluído e evento registrado.')
    return redirect('rastreamento:rota', frete_id=ponto.frete_id)
