from django.contrib import admin
from .models import WebhookEvento
@admin.register(WebhookEvento)
class WebhookEventoAdmin(admin.ModelAdmin):
    list_display=('id','__str__')
