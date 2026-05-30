from django.urls import path
from .views import TransportadoraListView,TransportadoraDetailView,TransportadoraCreateView,TransportadoraUpdateView,TransportadoraDeleteView
app_name='transportadoras'
urlpatterns=[
    path('', TransportadoraListView.as_view(), name='list'),
    path('novo/', TransportadoraCreateView.as_view(), name='create'),
    path('<int:pk>/', TransportadoraDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', TransportadoraUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', TransportadoraDeleteView.as_view(), name='delete'),
]
