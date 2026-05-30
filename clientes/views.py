from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from core.permissions import PapelRequiredMixin
from .forms import ClienteForm
from .models import Cliente

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'crud/list.html'
    paginate_by = 20

    def get_queryset(self):
        qs = Cliente.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(nome__icontains=q) | qs.filter(documento__icontains=q) | qs.filter(contato_principal__icontains=q)
        return qs.order_by('nome')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({'titulo': 'Clientes', 'create_url': 'clientes:create'})
        return ctx

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'crud/detail.html'
    context_object_name = 'objeto'

class ClienteCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos = ['ADMIN', 'OPERADOR']
    model = Cliente
    form_class = ClienteForm
    template_name = 'crud/form.html'
    success_url = reverse_lazy('clientes:list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Novo cliente'
        return ctx

class ClienteUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos = ['ADMIN', 'OPERADOR']
    model = Cliente
    form_class = ClienteForm
    template_name = 'crud/form.html'
    success_url = reverse_lazy('clientes:list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar cliente'
        return ctx

class ClienteDeleteView(LoginRequiredMixin, PapelRequiredMixin, DeleteView):
    papeis_permitidos = ['ADMIN']
    model = Cliente
    template_name = 'crud/confirm_delete.html'
    success_url = reverse_lazy('clientes:list')
