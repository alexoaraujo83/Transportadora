from django.urls import path
from .views import painel_seguranca
urlpatterns=[path('', painel_seguranca, name='painel_seguranca')]
