from django.contrib import admin
from .models import EventoRastreamento, PontoRota, PosicaoAtualFrete

@admin.register(EventoRastreamento)
class EventoRastreamentoAdmin(admin.ModelAdmin):
    list_display=('frete','tipo','descricao','latitude','longitude','origem_evento','criado_em')
    list_filter=('tipo','origem_evento','criado_em')
    search_fields=('descricao','frete__origem','frete__destino')

@admin.register(PontoRota)
class PontoRotaAdmin(admin.ModelAdmin):
    list_display=('frete','sequencia','nome','concluido','previsto_em','realizado_em')
    list_filter=('concluido',)
    search_fields=('nome','endereco','frete__origem','frete__destino')

@admin.register(PosicaoAtualFrete)
class PosicaoAtualFreteAdmin(admin.ModelAdmin):
    list_display=('frete','latitude','longitude','velocidade_kmh','atualizado_em')
    search_fields=('frete__origem','frete__destino','descricao')
