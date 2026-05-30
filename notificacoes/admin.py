from django.contrib import admin
from .models import Notificacao

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display=('titulo','usuario','canal','prioridade','lida','enviada_tempo_real','criada_em')
    list_filter=('canal','prioridade','lida','enviada_tempo_real','criada_em')
    search_fields=('titulo','mensagem','usuario__username')
