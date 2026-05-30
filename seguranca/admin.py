from django.contrib import admin
from .models import EventoSeguranca, PoliticaAcesso

@admin.register(EventoSeguranca)
class EventoSegurancaAdmin(admin.ModelAdmin):
    list_display=('tipo','severidade','usuario','ip','metodo','caminho','criado_em')
    list_filter=('tipo','severidade','criado_em')
    search_fields=('usuario__username','ip','caminho','detalhe')
    readonly_fields=('criado_em',)

@admin.register(PoliticaAcesso)
class PoliticaAcessoAdmin(admin.ModelAdmin):
    list_display=('perfil','modulo','pode_visualizar','pode_criar','pode_editar','pode_excluir','pode_exportar','ativo')
    list_filter=('perfil','modulo','ativo')
