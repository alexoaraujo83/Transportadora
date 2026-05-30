from django.urls import path
from .views import WebhookReceiverView
app_name='webhooks'
urlpatterns=[path('receber/<str:origem>/', WebhookReceiverView.as_view(), name='receber')]
