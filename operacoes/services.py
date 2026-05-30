from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from fretes.models import Frete
from financeiro.models import LancamentoFinanceiro
from notificacoes.models import Notificacao
from rastreamento.models import EventoRastreamento
from .models import ChecklistOperacional, HistoricoStatusFrete, ConsultaRisco

class FluxoFreteService:
    @staticmethod
    @transaction.atomic
    def alterar_status(frete, novo_status, usuario=None, observacao=''):
        anterior = frete.status
        if anterior == novo_status:
            return frete
        frete.status = novo_status
        frete.save(update_fields=['status','atualizado_em'])
        HistoricoStatusFrete.objects.create(
            frete=frete, status_anterior=anterior, status_novo=novo_status,
            usuario=usuario if getattr(usuario, 'is_authenticated', False) else None,
            observacao=observacao,
        )
        ChecklistOperacional.objects.get_or_create(frete=frete)
        Notificacao.objects.create(titulo='Status do frete atualizado', mensagem=f'Frete #{frete.id}: {anterior} → {novo_status}')
        return frete

    @staticmethod
    @transaction.atomic
    def converter_cotacao_em_frete(cotacao, usuario=None):
        frete = Frete.objects.create(
            origem=cotacao.origem, destino=cotacao.destino, carga=cotacao.carga,
            peso_kg=cotacao.peso_kg, cubagem_m3=cotacao.cubagem_m3,
            valor_cliente=cotacao.valor_sugerido, valor_motorista=Decimal('0.00'),
            status=Frete.Status.ABERTO,
            observacoes=f'Gerado automaticamente da cotação #{cotacao.id}. Solicitante: {cotacao.solicitante}. Contato: {cotacao.contato}',
        )
        cotacao.aprovada = True
        cotacao.save(update_fields=['aprovada'])
        ChecklistOperacional.objects.create(frete=frete)
        HistoricoStatusFrete.objects.create(frete=frete, status_anterior='', status_novo=frete.status, usuario=usuario if getattr(usuario, 'is_authenticated', False) else None, observacao='Frete criado a partir de cotação.')
        return frete

    @staticmethod
    @transaction.atomic
    def registrar_coleta(frete, usuario=None, observacao='Coleta confirmada'):
        checklist, _ = ChecklistOperacional.objects.get_or_create(frete=frete)
        checklist.coleta_confirmada = True
        checklist.comprovante_coleta = True
        checklist.save()
        EventoRastreamento.objects.create(frete=frete, descricao=observacao)
        return FluxoFreteService.alterar_status(frete, Frete.Status.EM_TRANSITO, usuario, observacao)

    @staticmethod
    @transaction.atomic
    def registrar_descarga(frete, usuario=None, observacao='Descarga confirmada'):
        checklist, _ = ChecklistOperacional.objects.get_or_create(frete=frete)
        checklist.descarga_confirmada = True
        checklist.comprovante_descarga = True
        checklist.save()
        EventoRastreamento.objects.create(frete=frete, descricao=observacao)
        if frete.valor_cliente:
            LancamentoFinanceiro.objects.get_or_create(frete=frete, tipo='RECEITA', descricao=f'Receita frete #{frete.id}', defaults={'valor': frete.valor_cliente, 'pago': False})
        if frete.valor_motorista:
            LancamentoFinanceiro.objects.get_or_create(frete=frete, tipo='DESPESA', descricao=f'Repasse motorista frete #{frete.id}', defaults={'valor': frete.valor_motorista, 'pago': False})
        return FluxoFreteService.alterar_status(frete, Frete.Status.ENTREGUE, usuario, observacao)

class RiscoService:
    @staticmethod
    def consultar_motorista(motorista, frete=None):
        status = ConsultaRisco.Status.APROVADO if motorista.aprovado_risco else ConsultaRisco.Status.PENDENTE
        consulta = ConsultaRisco.objects.create(motorista=motorista, frete=frete, status=status, protocolo=f'LOCAL-{timezone.now().strftime("%Y%m%d%H%M%S")}', observacao='Consulta local preparada para integração externa.')
        if status == ConsultaRisco.Status.APROVADO:
            if frete:
                checklist, _ = ChecklistOperacional.objects.get_or_create(frete=frete)
                checklist.risco_aprovado = True
                checklist.documentos_motorista = True
                checklist.save()
        return consulta
