from django.urls import path
from .views import FreteListView,FreteDetailView,FreteCreateView,FreteUpdateView,FreteDeleteView,alterar_status
app_name='fretes'
urlpatterns=[
    path('', FreteListView.as_view(), name='list'),
    path('novo/', FreteCreateView.as_view(), name='create'),
    path('<int:pk>/', FreteDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', FreteUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', FreteDeleteView.as_view(), name='delete'),
    path('<int:pk>/status/<str:status>/', alterar_status, name='alterar_status'),
]
