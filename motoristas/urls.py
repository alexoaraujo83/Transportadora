from django.urls import path
from .views import MotoristaListView,MotoristaDetailView,MotoristaCreateView,MotoristaUpdateView,MotoristaDeleteView
app_name='motoristas'
urlpatterns=[
    path('', MotoristaListView.as_view(), name='list'),
    path('novo/', MotoristaCreateView.as_view(), name='create'),
    path('<int:pk>/', MotoristaDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', MotoristaUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', MotoristaDeleteView.as_view(), name='delete'),
]
