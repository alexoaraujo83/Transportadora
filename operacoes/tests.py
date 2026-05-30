from django.test import TestCase
from fretes.models import Frete
from motoristas.models import Motorista
from cotacoes.models import Cotacao
from .services import FluxoFreteService, RiscoService

class FluxoOperacionalTest(TestCase):
    def test_fluxo_coleta_descarga_e_financeiro(self):
        frete = Frete.objects.create(origem='SP', destino='MG', carga='Teste', valor_cliente=1000, valor_motorista=800)
        FluxoFreteService.registrar_coleta(frete)
        frete.refresh_from_db(); self.assertEqual(frete.status, Frete.Status.EM_TRANSITO)
        FluxoFreteService.registrar_descarga(frete)
        frete.refresh_from_db(); self.assertEqual(frete.status, Frete.Status.ENTREGUE)
        self.assertEqual(frete.lancamentofinanceiro_set.count(), 2)

    def test_conversao_cotacao(self):
        c = Cotacao.objects.create(solicitante='Cliente', origem='SP', destino='BA', carga='Carga', valor_sugerido=2000)
        f = FluxoFreteService.converter_cotacao_em_frete(c)
        self.assertEqual(f.origem, 'SP'); c.refresh_from_db(); self.assertTrue(c.aprovada)

    def test_consulta_risco_local(self):
        m = Motorista.objects.create(nome='Motorista', aprovado_risco=True)
        consulta = RiscoService.consultar_motorista(m)
        self.assertEqual(consulta.status, 'APROVADO')
