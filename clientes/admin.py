from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_pessoa', 'documento', 'telefone', 'email', 'ativo')
    search_fields = ('nome', 'documento', 'telefone', 'email', 'contato_principal')
    list_filter = ('tipo_pessoa', 'ativo')
