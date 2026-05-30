from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from core.permissions import PapelRequiredMixin
from .models import Motorista
from core.forms import MotoristaForm

class MotoristaListView(LoginRequiredMixin, ListView):
    model=Motorista; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=20
    def get_queryset(self):
        qs=super().get_queryset().order_by('-id')
        q=self.request.GET.get('q')
        if q and hasattr(self.model,'nome'):
            qs=qs.filter(nome__icontains=q)
        return qs
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Motoristas','base_url':'motoristas','create_url':'motoristas:create'}); return ctx
class MotoristaDetailView(LoginRequiredMixin, DetailView): model=Motorista; template_name='crud/detail.html'; context_object_name='objeto'
class MotoristaCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=Motorista; form_class=MotoristaForm; template_name='crud/form.html'; success_url=reverse_lazy('motoristas:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Novo registro - Motoristas'; return ctx
class MotoristaUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=Motorista; form_class=MotoristaForm; template_name='crud/form.html'; success_url=reverse_lazy('motoristas:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Editar - Motoristas'; return ctx
class MotoristaDeleteView(LoginRequiredMixin, PapelRequiredMixin, DeleteView):
    papeis_permitidos=['ADMIN']; model=Motorista; template_name='crud/confirm_delete.html'; success_url=reverse_lazy('motoristas:list')
