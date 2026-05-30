from decimal import Decimal
from django.db.models import Avg, Count, Sum, Q
from fretes.models import Frete
from financeiro.models import ContaPagarReceber
from .models import InsightOperacional, PrevisaoFrete, ScoreMotorista

class InteligenciaOperacionalService:
    @staticmethod
    def sugerir_preco(frete):
        historico=Frete.objects.filter(origem__icontains=frete.origem.split('/')[0], destino__icontains=frete.destino.split('/')[0]).exclude(id=frete.id)
        media_cliente=historico.aggregate(v=Avg('valor_cliente'))['v'] or Decimal('0')
        media_motorista=historico.aggregate(v=Avg('valor_motorista'))['v'] or Decimal('0')
        base=media_cliente or (frete.valor_motorista * Decimal('1.22')) or Decimal('0')
        cubagem_extra=max(Decimal('0'), (frete.cubagem_m3 or Decimal('0'))-Decimal('20'))*Decimal('20')
        peso_extra=max(Decimal('0'), (frete.peso_kg or Decimal('0'))-Decimal('15000'))*Decimal('0.03')
        ideal=base+cubagem_extra+peso_extra
        minimo=ideal*Decimal('0.92')
        maximo=ideal*Decimal('1.15')
        margem=ideal-(frete.valor_motorista or Decimal('0'))
        risco=InteligenciaOperacionalService.calcular_risco_frete(frete)
        previsao,_=PrevisaoFrete.objects.update_or_create(
            frete=frete,
            defaults={
                'valor_sugerido_min':minimo,
                'valor_sugerido_ideal':ideal,
                'valor_sugerido_max':maximo,
                'margem_prevista':margem,
                'risco_operacional':risco,
                'explicacao':'Cálculo heurístico baseado em histórico de rota, valor motorista, peso, cubagem e risco operacional.'
            }
        )
        return previsao

    @staticmethod
    def calcular_risco_frete(frete):
        risco=Decimal('10')
        if not frete.motorista: risco += Decimal('25')
        elif not frete.motorista.aprovado_risco: risco += Decimal('35')
        if (frete.valor_cliente or Decimal('0')) <= (frete.valor_motorista or Decimal('0')): risco += Decimal('20')
        if (frete.peso_kg or Decimal('0')) > Decimal('30000'): risco += Decimal('10')
        if not frete.data_coleta: risco += Decimal('5')
        return min(risco, Decimal('100'))

    @staticmethod
    def gerar_insights():
        criados=[]
        for frete in Frete.objects.all()[:200]:
            previsao=InteligenciaOperacionalService.sugerir_preco(frete)
            if previsao.risco_operacional >= Decimal('60'):
                obj,_=InsightOperacional.objects.get_or_create(
                    frete=frete, tipo='RISCO', titulo=f'Risco elevado no frete {frete.id}', resolvido=False,
                    defaults={'severidade':'ALTA','score':previsao.risco_operacional,'descricao':f'Risco operacional estimado em {previsao.risco_operacional}%. Verificar motorista, aprovação de risco, margem e coleta.'}
                ); criados.append(obj)
            if previsao.margem_prevista <= Decimal('0'):
                obj,_=InsightOperacional.objects.get_or_create(
                    frete=frete, tipo='MARGEM', titulo=f'Margem negativa no frete {frete.id}', resolvido=False,
                    defaults={'severidade':'CRITICA','score':100,'descricao':'Valor cliente está igual ou abaixo do custo motorista. Renegociar antes de fechar.'}
                ); criados.append(obj)
        return criados

    @staticmethod
    def kpis_inteligencia():
        total=Frete.objects.count()
        margem_media=Frete.objects.aggregate(v=Avg('valor_cliente'))['v'] or Decimal('0')
        insights_abertos=InsightOperacional.objects.filter(resolvido=False).count()
        pendencias_financeiras=ContaPagarReceber.objects.filter(status__in=['ABERTA','PARCIAL','VENCIDA']).count()
        return {'fretes_analisados':total,'ticket_medio_cliente':margem_media,'insights_abertos':insights_abertos,'pendencias_financeiras':pendencias_financeiras}
