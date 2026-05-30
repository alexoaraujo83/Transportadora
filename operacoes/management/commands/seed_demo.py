from django.core.management.base import BaseCommand
from motoristas.models import Motorista
from transportadoras.models import Transportadora
from fretes.models import Frete

class Command(BaseCommand):
    help='Cria dados demonstrativos para teste local do Fusion Cargas Inteligente.'
    def handle(self, *args, **options):
        mot, _ = Motorista.objects.get_or_create(nome='Motorista Demo', defaults={'telefone':'(11) 99999-0000','placa':'ABC1D23','veiculo':'Carreta LS','carroceria':'Grade Baixa','aprovado_risco':True})
        transp, _ = Transportadora.objects.get_or_create(nome='Fusion Transportes Demo', defaults={'cnpj':'00.000.000/0001-00','email':'operacao@fusion.local','rntrc':'DEMO123'})
        Frete.objects.get_or_create(origem='São Paulo/SP', destino='Belo Horizonte/MG', carga='Carga paletizada', defaults={'peso_kg':28000,'cubagem_m3':80,'valor_motorista':3500,'valor_cliente':4300,'motorista':mot,'transportadora':transp,'status':'AGENDADO'})
        self.stdout.write(self.style.SUCCESS('Dados demonstrativos criados.'))
