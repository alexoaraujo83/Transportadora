from django.urls import path
from .views import central_notificacoes
app_name='notificacoes'
urlpatterns=[path('',central_notificacoes,name='central')]
