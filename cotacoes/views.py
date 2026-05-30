from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from core.permissions import PapelRequiredMixin
from .models import Cotacao
from core.forms import CotacaoForm

class CotacaoListView(LoginRequiredMixin, ListView):
    model=Cotacao; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=20
    def get_queryset(self):
        qs=super().get_queryset().order_by('-id')
        q=self.request.GET.get('q')
        if q and hasattr(self.model,'nome'):
            qs=qs.filter(nome__icontains=q)
        return qs
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Cotações','base_url':'cotacoes','create_url':'cotacoes:create'}); return ctx
class CotacaoDetailView(LoginRequiredMixin, DetailView): model=Cotacao; template_name='crud/detail.html'; context_object_name='objeto'
class CotacaoCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=Cotacao; form_class=CotacaoForm; template_name='crud/form.html'; success_url=reverse_lazy('cotacoes:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Novo registro - Cotações'; return ctx
class CotacaoUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=Cotacao; form_class=CotacaoForm; template_name='crud/form.html'; success_url=reverse_lazy('cotacoes:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Editar - Cotações'; return ctx
class CotacaoDeleteView(LoginRequiredMixin, PapelRequiredMixin, DeleteView):
    papeis_permitidos=['ADMIN']; model=Cotacao; template_name='crud/confirm_delete.html'; success_url=reverse_lazy('cotacoes:list')
