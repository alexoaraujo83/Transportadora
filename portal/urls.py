from django.urls import path
from . import views
urlpatterns=[
    path('frete/<str:token>/', views.consulta_frete, name='portal_consulta_frete'),
    path('frete/<str:token>/aceitar/', views.aceitar_frete, name='portal_aceitar_frete'),
    path('frete/<str:token>/comprovante/', views.enviar_comprovante, name='portal_enviar_comprovante'),
]
