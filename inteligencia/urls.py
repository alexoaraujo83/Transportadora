from django.urls import path
from .views import painel_inteligencia
urlpatterns=[path('', painel_inteligencia, name='painel_inteligencia')]
