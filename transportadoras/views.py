from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from core.permissions import PapelRequiredMixin
from .models import Transportadora
from core.forms import TransportadoraForm

class TransportadoraListView(LoginRequiredMixin, ListView):
    model=Transportadora; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=20
    def get_queryset(self):
        qs=super().get_queryset().order_by('-id')
        q=self.request.GET.get('q')
        if q and hasattr(self.model,'nome'):
            qs=qs.filter(nome__icontains=q)
        return qs
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Transportadoras','base_url':'transportadoras','create_url':'transportadoras:create'}); return ctx
class TransportadoraDetailView(LoginRequiredMixin, DetailView): model=Transportadora; template_name='crud/detail.html'; context_object_name='objeto'
class TransportadoraCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=Transportadora; form_class=TransportadoraForm; template_name='crud/form.html'; success_url=reverse_lazy('transportadoras:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Novo registro - Transportadoras'; return ctx
class TransportadoraUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=Transportadora; form_class=TransportadoraForm; template_name='crud/form.html'; success_url=reverse_lazy('transportadoras:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Editar - Transportadoras'; return ctx
class TransportadoraDeleteView(LoginRequiredMixin, PapelRequiredMixin, DeleteView):
    papeis_permitidos=['ADMIN']; model=Transportadora; template_name='crud/confirm_delete.html'; success_url=reverse_lazy('transportadoras:list')
