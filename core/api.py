from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from clientes.models import Cliente
from precificacao.models import TabelaPrecoRota, PropostaComercial
from precificacao.services import PrecificacaoService
from fretes.models import Frete
from motoristas.models import Motorista
from transportadoras.models import Transportadora
from cotacoes.models import Cotacao
from rastreamento.models import EventoRastreamento, PontoRota, PosicaoAtualFrete
from financeiro.models import LancamentoFinanceiro, ContaFinanceira, ContaPagarReceber, RepasseMotorista, ComissaoOperacional, ConciliacaoBancaria, FechamentoFinanceiro
from notificacoes.models import Notificacao
from webhooks.models import WebhookEvento
from auditoria.models import LogAuditoria
from .serializers import *
from rastreamento.services import RastreamentoService, MapasService
from .permissions import IsAdminOperadorOrReadOnly
from .kpis import calcular_kpis_operacionais
from financeiro.services import FinanceiroService

class BaseCrud(viewsets.ModelViewSet):
    permission_classes=[IsAdminOperadorOrReadOnly]
    ordering=['-id']

class ClienteViewSet(BaseCrud):
    queryset=Cliente.objects.all().order_by('nome')
    serializer_class=ClienteSerializer
    filterset_fields=['ativo','tipo_pessoa']
    search_fields=['nome','documento','telefone','email','contato_principal']

class TabelaPrecoRotaViewSet(BaseCrud):
    queryset=TabelaPrecoRota.objects.all().order_by('origem','destino')
    serializer_class=TabelaPrecoRotaSerializer
    filterset_fields=['ativa','veiculo','carroceria']
    search_fields=['origem','destino','veiculo','carroceria']

class PropostaComercialViewSet(BaseCrud):
    queryset=PropostaComercial.objects.select_related('cliente','rota').all().order_by('-criada_em')
    serializer_class=PropostaComercialSerializer
    filterset_fields=['status','cliente']
    search_fields=['cliente__nome','origem','destino','carga']

class SimuladorPrecificacaoAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request):
        data=request.data
        return Response(PrecificacaoService.simular(data.get('origem',''), data.get('destino',''), data.get('peso_kg',0), data.get('cubagem_m3',0), data.get('margem_percentual')))

class FreteViewSet(BaseCrud):
    queryset=Frete.objects.select_related('motorista','transportadora').all().order_by('-criado_em')
    serializer_class=FreteSerializer
    filterset_fields=['status','motorista','transportadora']
    search_fields=['origem','destino','carga','observacoes']
    ordering_fields=['criado_em','data_coleta','valor_motorista','valor_cliente']
class MotoristaViewSet(BaseCrud):
    queryset=Motorista.objects.all().order_by('-criado_em'); serializer_class=MotoristaSerializer
    filterset_fields=['ativo','aprovado_risco','carroceria']; search_fields=['nome','cpf','telefone','antt','placa','veiculo']
class TransportadoraViewSet(BaseCrud):
    queryset=Transportadora.objects.all().order_by('-criada_em'); serializer_class=TransportadoraSerializer
    filterset_fields=['ativa']; search_fields=['nome','cnpj','rntrc','email']
class CotacaoViewSet(BaseCrud):
    queryset=Cotacao.objects.all().order_by('-criada_em'); serializer_class=CotacaoSerializer
    filterset_fields=['aprovada']; search_fields=['solicitante','origem','destino','carga']
class RastreamentoViewSet(BaseCrud):
    queryset=EventoRastreamento.objects.select_related('frete').all().order_by('-criado_em'); serializer_class=EventoRastreamentoSerializer
    filterset_fields=['frete','tipo','origem_evento']; search_fields=['descricao','frete__origem','frete__destino']

    @action(detail=False, methods=['post'], url_path='registrar-posicao')
    def registrar_posicao(self, request):
        frete_id=request.data.get('frete')
        frete=Frete.objects.get(pk=frete_id)
        evento=RastreamentoService.registrar_posicao(
            frete=frete, descricao=request.data.get('descricao',''), latitude=request.data.get('latitude'), longitude=request.data.get('longitude'),
            velocidade_kmh=request.data.get('velocidade_kmh'), odometro_km=request.data.get('odometro_km'), origem_evento=request.data.get('origem_evento','api')
        )
        return Response(EventoRastreamentoSerializer(evento).data)

class PontoRotaViewSet(BaseCrud):
    queryset=PontoRota.objects.select_related('frete').all().order_by('frete','sequencia')
    serializer_class=PontoRotaSerializer
    filterset_fields=['frete','concluido']
    search_fields=['nome','endereco','frete__origem','frete__destino']

    @action(detail=True, methods=['post'], url_path='concluir')
    def concluir(self, request, pk=None):
        evento=RastreamentoService.concluir_ponto(self.get_object())
        return Response(EventoRastreamentoSerializer(evento).data)

class PosicaoAtualFreteViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes=[IsAdminOperadorOrReadOnly]
    queryset=PosicaoAtualFrete.objects.select_related('frete').all().order_by('-atualizado_em')
    serializer_class=PosicaoAtualFreteSerializer
    filterset_fields=['frete']
    search_fields=['descricao','frete__origem','frete__destino']
class FinanceiroViewSet(BaseCrud):
    queryset=LancamentoFinanceiro.objects.select_related('frete').all().order_by('-criado_em'); serializer_class=LancamentoFinanceiroSerializer
    filterset_fields=['tipo','pago','frete']; search_fields=['descricao']

class ContaFinanceiraViewSet(BaseCrud):
    queryset=ContaFinanceira.objects.all().order_by('nome')
    serializer_class=ContaFinanceiraSerializer
    filterset_fields=['tipo','ativa']
    search_fields=['nome','banco','agencia','conta']

class ContaPagarReceberViewSet(BaseCrud):
    queryset=ContaPagarReceber.objects.select_related('frete','conta').all().order_by('vencimento')
    serializer_class=ContaPagarReceberSerializer
    filterset_fields=['natureza','status','frete','conta','categoria','centro_custo']
    search_fields=['descricao','documento','favorecido']
    @action(detail=True, methods=['post'], url_path='baixar')
    def baixar(self, request, pk=None):
        conta=self.get_object(); conta.baixar(request.data.get('valor'))
        return Response(ContaPagarReceberSerializer(conta).data)

class RepasseMotoristaViewSet(BaseCrud):
    queryset=RepasseMotorista.objects.select_related('frete','motorista').all().order_by('status','data_programada','id')
    serializer_class=RepasseMotoristaSerializer
    filterset_fields=['status','motorista','frete']
    search_fields=['motorista__nome','observacao']

class ComissaoOperacionalViewSet(BaseCrud):
    queryset=ComissaoOperacional.objects.select_related('frete','usuario').all().order_by('status','-criado_em')
    serializer_class=ComissaoOperacionalSerializer
    filterset_fields=['status','usuario','frete']

class ConciliacaoBancariaViewSet(BaseCrud):
    queryset=ConciliacaoBancaria.objects.select_related('conta','lancamento').all().order_by('-data_movimento')
    serializer_class=ConciliacaoBancariaSerializer
    filterset_fields=['status','conta']
    search_fields=['historico','documento']

class FechamentoFinanceiroViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes=[IsAdminOperadorOrReadOnly]
    queryset=FechamentoFinanceiro.objects.all().order_by('-competencia')
    serializer_class=FechamentoFinanceiroSerializer

class DREAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request):
        return Response(FinanceiroService.calcular_dre(request.GET.get('inicio'), request.GET.get('fim')))

class GerarContasFreteAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request, frete_id):
        frete=Frete.objects.get(pk=frete_id)
        contas=FinanceiroService.gerar_contas_do_frete(frete)
        return Response(ContaPagarReceberSerializer(contas, many=True).data)
class NotificacaoViewSet(BaseCrud):
    queryset=Notificacao.objects.all().order_by('-criada_em'); serializer_class=NotificacaoSerializer
    filterset_fields=['lida']; search_fields=['titulo','mensagem']
class WebhookEventoViewSet(BaseCrud):
    queryset=WebhookEvento.objects.all().order_by('-criado_em'); serializer_class=WebhookEventoSerializer
    filterset_fields=['origem','evento','processado']
class LogAuditoriaViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes=[permissions.IsAdminUser]
    queryset=LogAuditoria.objects.all().order_by('-criado_em'); serializer_class=LogAuditoriaSerializer
    search_fields=['usuario','metodo','caminho']
from operacoes.models import ChecklistOperacional, HistoricoStatusFrete, ConsultaRisco, DocumentoFrete, OcorrenciaOperacional, TarefaOperacional
from operacoes.services import FluxoFreteService, RiscoService

class ChecklistOperacionalViewSet(BaseCrud):
    queryset=ChecklistOperacional.objects.select_related('frete').all().order_by('-atualizado_em')
    serializer_class=ChecklistOperacionalSerializer
    filterset_fields=['frete','risco_aprovado','coleta_confirmada','descarga_confirmada','financeiro_conferido']

class HistoricoStatusFreteViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes=[IsAdminOperadorOrReadOnly]
    queryset=HistoricoStatusFrete.objects.select_related('frete','usuario').all().order_by('-criado_em')
    serializer_class=HistoricoStatusFreteSerializer
    filterset_fields=['frete','status_novo']
    search_fields=['observacao']

class ConsultaRiscoViewSet(BaseCrud):
    queryset=ConsultaRisco.objects.select_related('motorista','frete').all().order_by('-criado_em')
    serializer_class=ConsultaRiscoSerializer
    filterset_fields=['motorista','frete','status']
    search_fields=['motorista__nome','protocolo','observacao']

# Ações operacionais adicionadas ao FreteViewSet existente
FreteViewSet.checklist = action(detail=True, methods=['get'])(lambda self, request, pk=None: Response(ChecklistOperacionalSerializer(ChecklistOperacional.objects.get_or_create(frete=self.get_object())[0]).data))

def _mudar_status(self, request, pk=None):
    frete=self.get_object(); novo=request.data.get('status')
    if novo not in dict(Frete.Status.choices): return Response({'erro':'status inválido'}, status=400)
    FluxoFreteService.alterar_status(frete, novo, request.user, request.data.get('observacao',''))
    return Response(FreteSerializer(frete).data)
FreteViewSet.mudar_status = action(detail=True, methods=['post'], url_path='mudar-status')(_mudar_status)

def _registrar_coleta(self, request, pk=None):
    frete=FluxoFreteService.registrar_coleta(self.get_object(), request.user, request.data.get('observacao','Coleta confirmada via API'))
    return Response(FreteSerializer(frete).data)
FreteViewSet.registrar_coleta = action(detail=True, methods=['post'], url_path='registrar-coleta')(_registrar_coleta)

def _registrar_descarga(self, request, pk=None):
    frete=FluxoFreteService.registrar_descarga(self.get_object(), request.user, request.data.get('observacao','Descarga confirmada via API'))
    return Response(FreteSerializer(frete).data)
FreteViewSet.registrar_descarga = action(detail=True, methods=['post'], url_path='registrar-descarga')(_registrar_descarga)

class DocumentoFreteViewSet(BaseCrud):
    queryset=DocumentoFrete.objects.select_related('frete').all().order_by('-criado_em')
    serializer_class=DocumentoFreteSerializer
    filterset_fields=['frete','tipo','validado']
    search_fields=['numero','descricao','frete__origem','frete__destino']

class OcorrenciaOperacionalViewSet(BaseCrud):
    queryset=OcorrenciaOperacional.objects.select_related('frete','responsavel').all().order_by('-criado_em')
    serializer_class=OcorrenciaOperacionalSerializer
    filterset_fields=['frete','gravidade','status','responsavel']
    search_fields=['titulo','descricao','frete__origem','frete__destino']

class TarefaOperacionalViewSet(BaseCrud):
    queryset=TarefaOperacional.objects.select_related('frete','responsavel').all().order_by('concluida','prazo','-criado_em')
    serializer_class=TarefaOperacionalSerializer
    filterset_fields=['frete','concluida','responsavel']
    search_fields=['titulo','descricao','frete__origem','frete__destino']



def _mapa_frete(self, request, pk=None):
    frete=self.get_object()
    pontos=PontoRota.objects.filter(frete=frete).order_by('sequencia')
    posicao=getattr(frete, 'posicao_atual', None)
    return Response({
        'frete': FreteSerializer(frete).data,
        'percentual_rota': RastreamentoService.calcular_percentual_rota(frete),
        'posicao_atual': PosicaoAtualFreteSerializer(posicao).data if posicao else None,
        'pontos': PontoRotaSerializer(pontos, many=True).data,
        'link_rota_google': MapasService.gerar_link_rota(pontos),
    })
FreteViewSet.mapa = action(detail=True, methods=['get'], url_path='mapa')(_mapa_frete)

class KpiOperacionalAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request):
        return Response(calcular_kpis_operacionais())
