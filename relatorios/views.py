import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Sum, Count
from fretes.models import Frete
from financeiro.models import LancamentoFinanceiro
from operacoes.models import ChecklistOperacional, OcorrenciaOperacional, DocumentoFrete, TarefaOperacional

@login_required
def painel_relatorios(request):
    por_status=Frete.objects.values('status').annotate(total=Count('id')).order_by('status')
    financeiro=LancamentoFinanceiro.objects.values('tipo','pago').annotate(total=Sum('valor'), quantidade=Count('id'))
    return render(request,'relatorios/painel.html', {'por_status':por_status,'financeiro':financeiro, 'ocorrencias_abertas': OcorrenciaOperacional.objects.exclude(status__in=['RESOLVIDA','CANCELADA']).count(), 'tarefas_pendentes': TarefaOperacional.objects.filter(concluida=False).count(), 'documentos_pendentes': DocumentoFrete.objects.filter(validado=False).count()})

@login_required
def exportar_fretes_csv(request):
    response=HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="fretes.csv"'
    response.write('﻿')
    writer=csv.writer(response, delimiter=';')
    writer.writerow(['ID','Origem','Destino','Carga','Status','Valor Motorista','Valor Cliente','Margem'])
    for f in Frete.objects.all().order_by('-criado_em'):
        writer.writerow([f.id,f.origem,f.destino,f.carga,f.status,f.valor_motorista,f.valor_cliente,f.margem])
    return response

@login_required
def exportar_financeiro_csv(request):
    response=HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="financeiro.csv"'
    response.write('﻿')
    writer=csv.writer(response, delimiter=';')
    writer.writerow(['ID','Frete','Tipo','Descrição','Valor','Vencimento','Pago'])
    for l in LancamentoFinanceiro.objects.select_related('frete').order_by('-criado_em'):
        writer.writerow([l.id,l.frete_id,l.tipo,l.descricao,l.valor,l.vencimento,'Sim' if l.pago else 'Não'])
    return response

@login_required
def exportar_operacional_csv(request):
    from operacoes.models import ChecklistOperacional
    response=HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="operacional_checklists.csv"'
    response.write('﻿')
    writer=csv.writer(response, delimiter=';')
    writer.writerow(['Frete','Rota','Percentual','Risco','Coleta','Descarga','Financeiro','Ocorrências'])
    for c in ChecklistOperacional.objects.select_related('frete').order_by('-atualizado_em'):
        writer.writerow([c.frete_id, f'{c.frete.origem} x {c.frete.destino}', c.percentual, c.risco_aprovado, c.coleta_confirmada, c.descarga_confirmada, c.financeiro_conferido, c.ocorrencias_pendentes])
    return response


@login_required
def exportar_ocorrencias_csv(request):
    response=HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="ocorrencias.csv"'
    response.write('﻿')
    writer=csv.writer(response, delimiter=';')
    writer.writerow(['ID','Frete','Título','Gravidade','Status','Responsável','Criado em'])
    for o in OcorrenciaOperacional.objects.select_related('frete','responsavel').order_by('-criado_em'):
        writer.writerow([o.id,o.frete_id,o.titulo,o.gravidade,o.status,getattr(o.responsavel,'username',''),o.criado_em])
    return response

@login_required
def exportar_documentos_csv(request):
    response=HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="documentos_frete.csv"'
    response.write('﻿')
    writer=csv.writer(response, delimiter=';')
    writer.writerow(['ID','Frete','Tipo','Número','Validado','URL'])
    for d in DocumentoFrete.objects.select_related('frete').order_by('-criado_em'):
        writer.writerow([d.id,d.frete_id,d.tipo,d.numero,'Sim' if d.validado else 'Não',d.arquivo_url])
    return response
