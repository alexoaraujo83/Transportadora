from django.test import TestCase
from fretes.models import Frete
class FreteModelTest(TestCase):
    def test_margem(self):
        f=Frete.objects.create(origem='SP', destino='MG', carga='Teste', valor_cliente=1500, valor_motorista=1000)
        self.assertEqual(f.margem, 500)
