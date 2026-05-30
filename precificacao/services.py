from decimal import Decimal
from .models import TabelaPrecoRota

class PrecificacaoService:
    @staticmethod
    def simular(origem, destino, peso_kg=0, cubagem_m3=0, margem_percentual=None):
        rota = TabelaPrecoRota.objects.filter(origem__icontains=origem, destino__icontains=destino, ativa=True).first()
        if not rota:
            return {
                'encontrou_tabela': False,
                'origem': origem,
                'destino': destino,
                'valor_motorista': Decimal('0.00'),
                'valor_cliente': Decimal('0.00'),
                'margem': Decimal('0.00'),
                'observacao': 'Não existe tabela cadastrada para esta rota.'
            }
        margem = Decimal(str(margem_percentual)) if margem_percentual is not None else rota.margem_percentual
        custo_base = rota.valor_minimo_motorista + rota.pedagio_estimado + rota.custo_extra_estimado
        valor_cliente = rota.valor_sugerido_cliente if rota.valor_sugerido_cliente > 0 else custo_base * (Decimal('1') + margem / Decimal('100'))
        return {
            'encontrou_tabela': True,
            'rota_id': rota.id,
            'origem': rota.origem,
            'destino': rota.destino,
            'veiculo': rota.veiculo,
            'carroceria': rota.carroceria,
            'valor_motorista': rota.valor_minimo_motorista,
            'pedagio_estimado': rota.pedagio_estimado,
            'custo_extra_estimado': rota.custo_extra_estimado,
            'valor_cliente': valor_cliente.quantize(Decimal('0.01')),
            'margem': (valor_cliente - rota.valor_minimo_motorista).quantize(Decimal('0.01')),
            'peso_kg': Decimal(str(peso_kg or 0)),
            'cubagem_m3': Decimal(str(cubagem_m3 or 0)),
        }
