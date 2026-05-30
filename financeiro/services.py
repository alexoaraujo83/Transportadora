from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from fretes.models import Frete
from .models import ContaPagarReceber, RepasseMotorista, ComissaoOperacional, FechamentoFinanceiro

class FinanceiroService:
    @staticmethod
    def gerar_contas_do_frete(frete: Frete):
        contas=[]
        if frete.valor_cliente:
            contas.append(ContaPagarReceber.objects.get_or_create(
                frete=frete, natureza=ContaPagarReceber.Natureza.RECEBER,
                descricao=f'Recebimento cliente - Frete {frete.id}',
                defaults={'valor_original': frete.valor_cliente, 'vencimento': frete.data_coleta or timezone.localdate(), 'favorecido': frete.origem}
            )[0])
        if frete.valor_motorista:
            contas.append(ContaPagarReceber.objects.get_or_create(
                frete=frete, natureza=ContaPagarReceber.Natureza.PAGAR,
                descricao=f'Repasse motorista - Frete {frete.id}',
                defaults={'valor_original': frete.valor_motorista, 'vencimento': frete.data_coleta or timezone.localdate(), 'favorecido': getattr(frete.motorista,'nome','Motorista') if frete.motorista else 'Motorista'}
            )[0])
            RepasseMotorista.objects.get_or_create(
                frete=frete,
                defaults={'motorista': frete.motorista, 'valor_frete': frete.valor_motorista}
            )
        return contas

    @staticmethod
    def calcular_dre(data_inicio=None, data_fim=None):
        qs=ContaPagarReceber.objects.exclude(status=ContaPagarReceber.Status.CANCELADA)
        if data_inicio: qs=qs.filter(vencimento__gte=data_inicio)
        if data_fim: qs=qs.filter(vencimento__lte=data_fim)
        receitas=qs.filter(natureza='RECEBER').aggregate(total=Sum('valor_original'))['total'] or Decimal('0')
        despesas=qs.filter(natureza='PAGAR').aggregate(total=Sum('valor_original'))['total'] or Decimal('0')
        lucro=receitas-despesas
        margem=(lucro/receitas*Decimal('100')) if receitas else Decimal('0')
        return {'receitas': receitas, 'despesas': despesas, 'lucro_bruto': lucro, 'margem_percentual': margem}

    @staticmethod
    def criar_comissao(frete, usuario, percentual=Decimal('7.00'), sobre='margem'):
        base = frete.margem if sobre == 'margem' else frete.valor_cliente
        return ComissaoOperacional.objects.create(frete=frete, usuario=usuario, base_calculo=base or 0, percentual=percentual)

    @staticmethod
    def fechamento_mensal(competencia, usuario=None):
        inicio=f'{competencia}-01'
        from datetime import date
        ano, mes = [int(x) for x in competencia.split('-')]
        fim = date(ano + (mes//12), (mes%12)+1, 1) if mes < 12 else date(ano+1,1,1)
        dre=FinanceiroService.calcular_dre(inicio, fim)
        obj,_=FechamentoFinanceiro.objects.update_or_create(
            competencia=competencia,
            defaults={**dre, 'fechado_por': usuario}
        )
        return obj
