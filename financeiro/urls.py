from django.urls import path
from .views import *
app_name='financeiro'
urlpatterns=[
    path('', FinanceiroDashboardView.as_view(), name='dashboard'),
    path('lancamentos/', LancamentoFinanceiroListView.as_view(), name='list'),
    path('lancamentos/novo/', LancamentoFinanceiroCreateView.as_view(), name='create'),
    path('lancamentos/<int:pk>/', LancamentoFinanceiroDetailView.as_view(), name='detail'),
    path('lancamentos/<int:pk>/editar/', LancamentoFinanceiroUpdateView.as_view(), name='update'),
    path('lancamentos/<int:pk>/excluir/', LancamentoFinanceiroDeleteView.as_view(), name='delete'),
    path('contas/', ContaPagarReceberListView.as_view(), name='contas'),
    path('repasses/', RepasseMotoristaListView.as_view(), name='repasses'),
    path('comissoes/', ComissaoOperacionalListView.as_view(), name='comissoes'),
    path('conciliacao/', ConciliacaoBancariaListView.as_view(), name='conciliacao'),
    path('relatorios/dre.csv', dre_csv, name='dre_csv'),
    path('relatorios/contas.csv', contas_csv, name='contas_csv'),
]
