from django.core.management.base import BaseCommand
from seguranca.models import PoliticaAcesso

class Command(BaseCommand):
    help='Cria políticas padrão de acesso por perfil.'
    def handle(self,*args,**kwargs):
        perfis=['ADMIN','OPERADOR','CLIENTE','MOTORISTA','TRANSPORTADORA']
        modulos=['fretes','motoristas','transportadoras','cotacoes','financeiro','relatorios','rastreamento','operacoes','clientes','precificacao']
        for perfil in perfis:
            for modulo in modulos:
                data={'pode_visualizar': True, 'pode_criar': perfil in ['ADMIN','OPERADOR'], 'pode_editar': perfil in ['ADMIN','OPERADOR'], 'pode_excluir': perfil == 'ADMIN', 'pode_exportar': perfil in ['ADMIN','OPERADOR']}
                if perfil == 'CLIENTE': data.update({'pode_criar': modulo in ['cotacoes'], 'pode_editar': False, 'pode_excluir': False, 'pode_exportar': False})
                if perfil == 'MOTORISTA': data.update({'pode_visualizar': modulo in ['fretes','rastreamento','operacoes'], 'pode_criar': modulo in ['rastreamento'], 'pode_editar': False, 'pode_excluir': False, 'pode_exportar': False})
                PoliticaAcesso.objects.update_or_create(perfil=perfil, modulo=modulo, defaults=data)
        self.stdout.write(self.style.SUCCESS('Políticas padrão criadas/atualizadas.'))
