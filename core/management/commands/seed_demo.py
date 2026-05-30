from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from motoristas.models import Motorista
from transportadoras.models import Transportadora
from fretes.models import Frete
from financeiro.models import LancamentoFinanceiro
from operacoes.models import ChecklistOperacional, TarefaOperacional, OcorrenciaOperacional, DocumentoFrete


class Command(BaseCommand):
    help = 'Cria dados demonstrativos seguros para validar fluxo operacional do Fusion Cargas.'

    def handle(self, *args, **options):
        motorista, _ = Motorista.objects.get_or_create(
            cpf='00000000000',
            defaults={
                'nome': 'Motorista Demonstração', 'telefone': '(11) 99999-0000',
                'antt': 'ANTT-DEMO', 'placa': 'ABC1D23', 'veiculo': 'Carreta LS',
                'carroceria': 'Grade Baixa', 'aprovado_risco': True, 'ativo': True,
            },
        )
        transportadora, _ = Transportadora.objects.get_or_create(
            cnpj='00000000000100',
            defaults={'nome': 'Transportadora Demonstração', 'telefone': '(11) 3000-0000', 'email': 'demo@fusion.local', 'rntrc': 'RNTRC-DEMO', 'ativa': True},
        )
        frete, _ = Frete.objects.get_or_create(
            origem='São Paulo/SP', destino='Belo Horizonte/MG', carga='Carga paletizada demonstração',
            defaults={
                'peso_kg': Decimal('12000'), 'cubagem_m3': Decimal('45'),
                'valor_motorista': Decimal('3500'), 'valor_cliente': Decimal('4300'),
                'forma_pagamento': '70/30 via PIX', 'data_coleta': timezone.now(),
                'motorista': motorista, 'transportadora': transportadora, 'status': Frete.Status.AGENDADO,
                'observacoes': 'Registro gerado pelo seed_demo para teste operacional.',
            },
        )
        ChecklistOperacional.objects.get_or_create(frete=frete, defaults={'documentos_motorista': True, 'risco_aprovado': True})
        LancamentoFinanceiro.objects.get_or_create(frete=frete, tipo='RECEITA', descricao='Receita demo cliente', defaults={'valor': Decimal('4300'), 'vencimento': timezone.now().date(), 'pago': False})
        LancamentoFinanceiro.objects.get_or_create(frete=frete, tipo='DESPESA', descricao='Repasse demo motorista', defaults={'valor': Decimal('3500'), 'vencimento': timezone.now().date(), 'pago': False})
        DocumentoFrete.objects.get_or_create(frete=frete, tipo='NFE', numero='DEMO-001', defaults={'descricao': 'Documento demonstrativo pendente de validação'})
        TarefaOperacional.objects.get_or_create(frete=frete, titulo='Confirmar horário de coleta', defaults={'descricao': 'Validar janela com embarcador e motorista.'})
        OcorrenciaOperacional.objects.get_or_create(frete=frete, titulo='Exemplo de ocorrência baixa', defaults={'descricao': 'Ocorrência criada para testar painel.', 'gravidade': 'BAIXA'})
        self.stdout.write(self.style.SUCCESS('Dados demonstrativos criados/atualizados com sucesso.'))
