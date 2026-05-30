from decimal import Decimal
from django.db.models import Count, Sum, Q
from fretes.models import Frete
from financeiro.models import LancamentoFinanceiro
from motoristas.models import Motorista
from operacoes.models import OcorrenciaOperacional, TarefaOperacional, DocumentoFrete, ChecklistOperacional


def calcular_kpis_operacionais():
    receitas = LancamentoFinanceiro.objects.filter(tipo='RECEITA', pago=True).aggregate(total=Sum('valor'))['total'] or Decimal('0')
    despesas = LancamentoFinanceiro.objects.filter(tipo='DESPESA', pago=True).aggregate(total=Sum('valor'))['total'] or Decimal('0')
    fretes_total = Frete.objects.count()
    fretes_entregues = Frete.objects.filter(status='ENTREGUE').count()
    margem_prevista = sum((f.margem for f in Frete.objects.all()), Decimal('0'))
    return {
        'fretes_total': fretes_total,
        'fretes_entregues': fretes_entregues,
        'taxa_entrega_percentual': round((fretes_entregues / fretes_total) * 100, 2) if fretes_total else 0,
        'fretes_em_transito': Frete.objects.filter(status='EM_TRANSITO').count(),
        'fretes_sem_motorista': Frete.objects.filter(motorista__isnull=True).exclude(status__in=['ENTREGUE','CANCELADO']).count(),
        'motoristas_ativos': Motorista.objects.filter(ativo=True).count(),
        'motoristas_aprovados_risco': Motorista.objects.filter(ativo=True, aprovado_risco=True).count(),
        'ocorrencias_abertas': OcorrenciaOperacional.objects.exclude(status__in=['RESOLVIDA','CANCELADA']).count(),
        'tarefas_pendentes': TarefaOperacional.objects.filter(concluida=False).count(),
        'documentos_pendentes_validacao': DocumentoFrete.objects.filter(validado=False).count(),
        'checklists_incompletos': sum(1 for c in ChecklistOperacional.objects.all() if c.percentual < 100),
        'receitas_pagas': receitas,
        'despesas_pagas': despesas,
        'saldo_pago': receitas - despesas,
        'margem_prevista_total': margem_prevista,
        'fretes_por_status': list(Frete.objects.values('status').annotate(total=Count('id')).order_by('status')),
    }
