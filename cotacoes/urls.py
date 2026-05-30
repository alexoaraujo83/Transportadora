from django.urls import path
from .views import CotacaoListView,CotacaoDetailView,CotacaoCreateView,CotacaoUpdateView,CotacaoDeleteView
app_name='cotacoes'
urlpatterns=[
    path('', CotacaoListView.as_view(), name='list'),
    path('novo/', CotacaoCreateView.as_view(), name='create'),
    path('<int:pk>/', CotacaoDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', CotacaoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', CotacaoDeleteView.as_view(), name='delete'),
]
