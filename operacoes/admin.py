from django.contrib import admin
from .models import ChecklistOperacional, HistoricoStatusFrete, ConsultaRisco, DocumentoFrete, OcorrenciaOperacional, TarefaOperacional
@admin.register(ChecklistOperacional)
class ChecklistOperacionalAdmin(admin.ModelAdmin):
    list_display=('frete','percentual','risco_aprovado','coleta_confirmada','descarga_confirmada','financeiro_conferido')
@admin.register(HistoricoStatusFrete)
class HistoricoStatusFreteAdmin(admin.ModelAdmin):
    list_display=('frete','status_anterior','status_novo','usuario','criado_em')
    search_fields=('frete__origem','frete__destino','observacao')
@admin.register(ConsultaRisco)
class ConsultaRiscoAdmin(admin.ModelAdmin):
    list_display=('motorista','frete','status','protocolo','criado_em')
    list_filter=('status',)

@admin.register(DocumentoFrete)
class DocumentoFreteAdmin(admin.ModelAdmin):
    list_display=('frete','tipo','numero','validado','criado_em')
    list_filter=('tipo','validado')
    search_fields=('numero','frete__origem','frete__destino')

@admin.register(OcorrenciaOperacional)
class OcorrenciaOperacionalAdmin(admin.ModelAdmin):
    list_display=('frete','titulo','gravidade','status','responsavel','criado_em')
    list_filter=('gravidade','status')
    search_fields=('titulo','descricao','frete__origem','frete__destino')

@admin.register(TarefaOperacional)
class TarefaOperacionalAdmin(admin.ModelAdmin):
    list_display=('frete','titulo','prazo','concluida','responsavel')
    list_filter=('concluida',)
    search_fields=('titulo','descricao','frete__origem','frete__destino')
