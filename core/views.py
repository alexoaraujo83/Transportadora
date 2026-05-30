from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from fretes.models import Frete
from motoristas.models import Motorista
from transportadoras.models import Transportadora
from cotacoes.models import Cotacao
from financeiro.models import LancamentoFinanceiro
from notificacoes.models import Notificacao
from operacoes.models import OcorrenciaOperacional, TarefaOperacional, DocumentoFrete
from clientes.models import Cliente
from precificacao.models import TabelaPrecoRota, PropostaComercial
from .kpis import calcular_kpis_operacionais

@login_required
def dashboard(request):
    receitas = LancamentoFinanceiro.objects.filter(tipo='RECEITA', pago=True).aggregate(total=Sum('valor'))['total'] or 0
    despesas = LancamentoFinanceiro.objects.filter(tipo='DESPESA', pago=True).aggregate(total=Sum('valor'))['total'] or 0
    ctx={
        'clientes_total': Cliente.objects.count(),
        'tabelas_preco_total': TabelaPrecoRota.objects.filter(ativa=True).count(),
        'propostas_abertas': PropostaComercial.objects.exclude(status__in=['APROVADA','RECUSADA','CANCELADA']).count(),
        'fretes_total': Frete.objects.count(),
        'fretes_abertos': Frete.objects.filter(status='ABERTO').count(),
        'fretes_transito': Frete.objects.filter(status='EM_TRANSITO').count(),
        'motoristas_total': Motorista.objects.count(),
        'motoristas_aprovados': Motorista.objects.filter(aprovado_risco=True).count(),
        'transportadoras_total': Transportadora.objects.count(),
        'cotacoes_total': Cotacao.objects.count(),
        'receitas': receitas,
        'despesas': despesas,
        'saldo': receitas-despesas,
        'fretes': Frete.objects.order_by('-criado_em')[:10],
        'notificacoes': Notificacao.objects.filter(lida=False).order_by('-criada_em')[:5],
        'por_status': Frete.objects.values('status').annotate(total=Count('id')),
        'ocorrencias_abertas': OcorrenciaOperacional.objects.exclude(status__in=['RESOLVIDA','CANCELADA']).count(),
        'tarefas_pendentes': TarefaOperacional.objects.filter(concluida=False).count(),
        'documentos_pendentes': DocumentoFrete.objects.filter(validado=False).count(),
        'kpis': calcular_kpis_operacionais(),
    }
    return render(request,'core/dashboard.html',ctx)
