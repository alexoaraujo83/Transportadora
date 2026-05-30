from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from core.permissions import PapelRequiredMixin
from .models import Frete
from core.forms import FreteForm

class FreteListView(LoginRequiredMixin, ListView):
    model=Frete; template_name='crud/list.html'; context_object_name='objetos'; paginate_by=20
    def get_queryset(self):
        qs=super().get_queryset().order_by('-id')
        q=self.request.GET.get('q')
        if q and hasattr(self.model,'nome'):
            qs=qs.filter(nome__icontains=q)
        return qs
    def get_context_data(self, **kwargs):
        ctx=super().get_context_data(**kwargs); ctx.update({'titulo':'Fretes','base_url':'fretes','create_url':'fretes:create'}); return ctx
class FreteDetailView(LoginRequiredMixin, DetailView): model=Frete; template_name='crud/detail.html'; context_object_name='objeto'
class FreteCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=Frete; form_class=FreteForm; template_name='crud/form.html'; success_url=reverse_lazy('fretes:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Novo registro - Fretes'; return ctx
class FreteUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos=['ADMIN','OPERADOR']; model=Frete; form_class=FreteForm; template_name='crud/form.html'; success_url=reverse_lazy('fretes:list')
    def get_context_data(self, **kwargs): ctx=super().get_context_data(**kwargs); ctx['titulo']='Editar - Fretes'; return ctx
class FreteDeleteView(LoginRequiredMixin, PapelRequiredMixin, DeleteView):
    papeis_permitidos=['ADMIN']; model=Frete; template_name='crud/confirm_delete.html'; success_url=reverse_lazy('fretes:list')

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def alterar_status(request, pk, status):
    frete=get_object_or_404(Frete, pk=pk)
    if status in dict(Frete.Status.choices):
        frete.status=status; frete.save(update_fields=['status','atualizado_em'])
        messages.success(request, f'Status alterado para {frete.get_status_display()}.')
    return redirect('fretes:detail', pk=pk)
