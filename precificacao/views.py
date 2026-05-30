from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from core.permissions import PapelRequiredMixin
from .forms import TabelaPrecoRotaForm, PropostaComercialForm
from .models import TabelaPrecoRota, PropostaComercial
from .services import PrecificacaoService

class TabelaPrecoListView(LoginRequiredMixin, ListView):
    model = TabelaPrecoRota
    template_name = 'crud/list.html'
    paginate_by = 20
    def get_queryset(self):
        qs = TabelaPrecoRota.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(origem__icontains=q) | qs.filter(destino__icontains=q) | qs.filter(veiculo__icontains=q)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({'titulo': 'Tabela de preços por rota', 'create_url': 'precificacao:tabela_create'})
        return ctx

class TabelaPrecoCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos = ['ADMIN', 'OPERADOR']
    model = TabelaPrecoRota
    form_class = TabelaPrecoRotaForm
    template_name = 'crud/form.html'
    success_url = reverse_lazy('precificacao:tabelas')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); ctx['titulo'] = 'Nova tabela de preço'; return ctx

class TabelaPrecoUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos = ['ADMIN', 'OPERADOR']
    model = TabelaPrecoRota
    form_class = TabelaPrecoRotaForm
    template_name = 'crud/form.html'
    success_url = reverse_lazy('precificacao:tabelas')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); ctx['titulo'] = 'Editar tabela de preço'; return ctx

class TabelaPrecoDeleteView(LoginRequiredMixin, PapelRequiredMixin, DeleteView):
    papeis_permitidos = ['ADMIN']
    model = TabelaPrecoRota
    template_name = 'crud/confirm_delete.html'
    success_url = reverse_lazy('precificacao:tabelas')

class PropostaListView(LoginRequiredMixin, ListView):
    model = PropostaComercial
    template_name = 'crud/list.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); ctx.update({'titulo': 'Propostas comerciais', 'create_url': 'precificacao:proposta_create'}); return ctx

class PropostaCreateView(LoginRequiredMixin, PapelRequiredMixin, CreateView):
    papeis_permitidos = ['ADMIN', 'OPERADOR']
    model = PropostaComercial
    form_class = PropostaComercialForm
    template_name = 'crud/form.html'
    success_url = reverse_lazy('precificacao:propostas')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); ctx['titulo'] = 'Nova proposta comercial'; return ctx

class PropostaUpdateView(LoginRequiredMixin, PapelRequiredMixin, UpdateView):
    papeis_permitidos = ['ADMIN', 'OPERADOR']
    model = PropostaComercial
    form_class = PropostaComercialForm
    template_name = 'crud/form.html'
    success_url = reverse_lazy('precificacao:propostas')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); ctx['titulo'] = 'Editar proposta comercial'; return ctx

def simulador(request):
    resultado = None
    if request.method == 'POST':
        resultado = PrecificacaoService.simular(
            request.POST.get('origem', ''),
            request.POST.get('destino', ''),
            request.POST.get('peso_kg') or 0,
            request.POST.get('cubagem_m3') or 0,
            request.POST.get('margem_percentual') or None,
        )
    return render(request, 'precificacao/simulador.html', {'resultado': resultado})
