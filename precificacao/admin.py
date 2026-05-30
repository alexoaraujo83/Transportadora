from django.contrib import admin
from .models import TabelaPrecoRota, PropostaComercial

@admin.register(TabelaPrecoRota)
class TabelaPrecoRotaAdmin(admin.ModelAdmin):
    list_display = ('origem', 'destino', 'veiculo', 'carroceria', 'valor_minimo_motorista', 'valor_sugerido_cliente', 'ativa')
    search_fields = ('origem', 'destino', 'veiculo', 'carroceria')
    list_filter = ('ativa', 'veiculo', 'carroceria')

@admin.register(PropostaComercial)
class PropostaComercialAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'origem', 'destino', 'valor_motorista', 'valor_cliente', 'status', 'criada_em')
    search_fields = ('cliente__nome', 'origem', 'destino', 'carga')
    list_filter = ('status',)
