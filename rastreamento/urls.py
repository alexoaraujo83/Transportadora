from django.urls import path
from .views import EventoRastreamentoListView,EventoRastreamentoDetailView,EventoRastreamentoCreateView,EventoRastreamentoUpdateView,EventoRastreamentoDeleteView,MapaFretesView,RotaFreteView,PontoRotaCreateView,concluir_ponto
app_name='rastreamento'
urlpatterns=[
    path('', EventoRastreamentoListView.as_view(), name='list'),
    path('mapa/', MapaFretesView.as_view(), name='mapa'),
    path('rota/<int:frete_id>/', RotaFreteView.as_view(), name='rota'),
    path('rota/ponto/novo/', PontoRotaCreateView.as_view(), name='ponto_create'),
    path('rota/ponto/<int:pk>/concluir/', concluir_ponto, name='ponto_concluir'),
    path('novo/', EventoRastreamentoCreateView.as_view(), name='create'),
    path('<int:pk>/', EventoRastreamentoDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', EventoRastreamentoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', EventoRastreamentoDeleteView.as_view(), name='delete'),
]
