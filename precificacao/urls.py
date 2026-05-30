from django.urls import path
from . import views

app_name = 'precificacao'
urlpatterns = [
    path('tabelas/', views.TabelaPrecoListView.as_view(), name='tabelas'),
    path('tabelas/nova/', views.TabelaPrecoCreateView.as_view(), name='tabela_create'),
    path('tabelas/<int:pk>/editar/', views.TabelaPrecoUpdateView.as_view(), name='tabela_update'),
    path('tabelas/<int:pk>/excluir/', views.TabelaPrecoDeleteView.as_view(), name='tabela_delete'),
    path('propostas/', views.PropostaListView.as_view(), name='propostas'),
    path('propostas/nova/', views.PropostaCreateView.as_view(), name='proposta_create'),
    path('propostas/<int:pk>/editar/', views.PropostaUpdateView.as_view(), name='proposta_update'),
    path('simulador/', views.simulador, name='simulador'),
]
