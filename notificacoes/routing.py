from django.urls import re_path
from .consumers import NotificacoesConsumer

websocket_urlpatterns=[
    re_path(r'ws/notificacoes/$', NotificacoesConsumer.as_asgi()),
]
