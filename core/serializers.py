from rest_framework import serializers
from clientes.models import Cliente
from precificacao.models import TabelaPrecoRota, PropostaComercial
from fretes.models import Frete
from motoristas.models import Motorista
from transportadoras.models import Transportadora
from cotacoes.models import Cotacao
from rastreamento.models import EventoRastreamento, PontoRota, PosicaoAtualFrete
from financeiro.models import LancamentoFinanceiro, ContaFinanceira, ContaPagarReceber, RepasseMotorista, ComissaoOperacional, ConciliacaoBancaria, FechamentoFinanceiro
from notificacoes.models import Notificacao
from webhooks.models import WebhookEvento
from auditoria.models import LogAuditoria

class ClienteSerializer(serializers.ModelSerializer):
    class Meta: model=Cliente; fields='__all__'

class TabelaPrecoRotaSerializer(serializers.ModelSerializer):
    valor_calculado_cliente=serializers.DecimalField(source='calcular_valor_cliente', max_digits=12, decimal_places=2, read_only=True)
    class Meta: model=TabelaPrecoRota; fields='__all__'

class PropostaComercialSerializer(serializers.ModelSerializer):
    margem=serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    cliente_nome=serializers.CharField(source='cliente.nome', read_only=True)
    class Meta: model=PropostaComercial; fields='__all__'

class FreteSerializer(serializers.ModelSerializer):
    margem=serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    motorista_nome=serializers.CharField(source='motorista.nome', read_only=True)
    transportadora_nome=serializers.CharField(source='transportadora.nome', read_only=True)
    class Meta: model=Frete; fields='__all__'
class MotoristaSerializer(serializers.ModelSerializer):
    class Meta: model=Motorista; fields='__all__'
class TransportadoraSerializer(serializers.ModelSerializer):
    class Meta: model=Transportadora; fields='__all__'
class CotacaoSerializer(serializers.ModelSerializer):
    class Meta: model=Cotacao; fields='__all__'
class EventoRastreamentoSerializer(serializers.ModelSerializer):
    frete_rota=serializers.CharField(source='frete.__str__', read_only=True)
    class Meta: model=EventoRastreamento; fields='__all__'

class PontoRotaSerializer(serializers.ModelSerializer):
    class Meta: model=PontoRota; fields='__all__'

class PosicaoAtualFreteSerializer(serializers.ModelSerializer):
    frete_rota=serializers.CharField(source='frete.__str__', read_only=True)
    class Meta: model=PosicaoAtualFrete; fields='__all__'
class LancamentoFinanceiroSerializer(serializers.ModelSerializer):
    class Meta: model=LancamentoFinanceiro; fields='__all__'
class ContaFinanceiraSerializer(serializers.ModelSerializer):
    class Meta: model=ContaFinanceira; fields='__all__'
class ContaPagarReceberSerializer(serializers.ModelSerializer):
    saldo=serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta: model=ContaPagarReceber; fields='__all__'
class RepasseMotoristaSerializer(serializers.ModelSerializer):
    motorista_nome=serializers.CharField(source='motorista.nome', read_only=True)
    class Meta: model=RepasseMotorista; fields='__all__'
class ComissaoOperacionalSerializer(serializers.ModelSerializer):
    usuario_nome=serializers.CharField(source='usuario.username', read_only=True)
    class Meta: model=ComissaoOperacional; fields='__all__'
class ConciliacaoBancariaSerializer(serializers.ModelSerializer):
    class Meta: model=ConciliacaoBancaria; fields='__all__'
class FechamentoFinanceiroSerializer(serializers.ModelSerializer):
    class Meta: model=FechamentoFinanceiro; fields='__all__'
class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta: model=Notificacao; fields='__all__'
class WebhookEventoSerializer(serializers.ModelSerializer):
    class Meta: model=WebhookEvento; fields='__all__'
class LogAuditoriaSerializer(serializers.ModelSerializer):
    class Meta: model=LogAuditoria; fields='__all__'

from operacoes.models import ChecklistOperacional, HistoricoStatusFrete, ConsultaRisco, DocumentoFrete, OcorrenciaOperacional, TarefaOperacional

class ChecklistOperacionalSerializer(serializers.ModelSerializer):
    percentual=serializers.IntegerField(read_only=True)
    class Meta: model=ChecklistOperacional; fields='__all__'
class HistoricoStatusFreteSerializer(serializers.ModelSerializer):
    usuario_nome=serializers.CharField(source='usuario.username', read_only=True)
    class Meta: model=HistoricoStatusFrete; fields='__all__'
class ConsultaRiscoSerializer(serializers.ModelSerializer):
    motorista_nome=serializers.CharField(source='motorista.nome', read_only=True)
    frete_rota=serializers.CharField(source='frete.__str__', read_only=True)
    class Meta: model=ConsultaRisco; fields='__all__'

class DocumentoFreteSerializer(serializers.ModelSerializer):
    class Meta: model=DocumentoFrete; fields='__all__'
class OcorrenciaOperacionalSerializer(serializers.ModelSerializer):
    responsavel_nome=serializers.CharField(source='responsavel.username', read_only=True)
    class Meta: model=OcorrenciaOperacional; fields='__all__'
class TarefaOperacionalSerializer(serializers.ModelSerializer):
    responsavel_nome=serializers.CharField(source='responsavel.username', read_only=True)
    class Meta: model=TarefaOperacional; fields='__all__'
