from django.core.management.base import BaseCommand
from inteligencia.services import InteligenciaOperacionalService
class Command(BaseCommand):
    help='Gera previsões e insights operacionais para fretes'
    def handle(self,*args,**kwargs):
        criados=InteligenciaOperacionalService.gerar_insights()
        self.stdout.write(self.style.SUCCESS(f'Insights verificados/criados: {len(criados)}'))
