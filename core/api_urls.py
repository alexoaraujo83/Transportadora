from django.urls import path
from rest_framework.routers import DefaultRouter
from .api import *

router=DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('tabelas-preco', TabelaPrecoRotaViewSet)
router.register('propostas-comerciais', PropostaComercialViewSet)
router.register('fretes', FreteViewSet)
router.register('motoristas', MotoristaViewSet)
router.register('transportadoras', TransportadoraViewSet)
router.register('cotacoes', CotacaoViewSet)
router.register('rastreamentos', RastreamentoViewSet)
router.register('pontos-rota', PontoRotaViewSet)
router.register('posicoes-atuais', PosicaoAtualFreteViewSet)
router.register('financeiro', FinanceiroViewSet)
router.register('contas-financeiras', ContaFinanceiraViewSet)
router.register('contas-pagar-receber', ContaPagarReceberViewSet)
router.register('repasses-motoristas', RepasseMotoristaViewSet)
router.register('comissoes-operacionais', ComissaoOperacionalViewSet)
router.register('conciliacoes-bancarias', ConciliacaoBancariaViewSet)
router.register('fechamentos-financeiros', FechamentoFinanceiroViewSet)
router.register('notificacoes', NotificacaoViewSet)
router.register('webhooks', WebhookEventoViewSet)
router.register('auditoria', LogAuditoriaViewSet)
router.register('checklists', ChecklistOperacionalViewSet)
router.register('historico-status', HistoricoStatusFreteViewSet)
router.register('consultas-risco', ConsultaRiscoViewSet)
router.register('documentos-frete', DocumentoFreteViewSet)
router.register('ocorrencias', OcorrenciaOperacionalViewSet)
router.register('tarefas', TarefaOperacionalViewSet)

urlpatterns=[path('kpis/', KpiOperacionalAPIView.as_view(), name='api-kpis'), path('dre/', DREAPIView.as_view(), name='api-dre'), path('fretes/<int:frete_id>/gerar-contas/', GerarContasFreteAPIView.as_view(), name='api-gerar-contas-frete'), path('simular-preco/', SimuladorPrecificacaoAPIView.as_view(), name='api-simular-preco')] + router.urls
