from django.db import models
from django.contrib.auth import get_user_model
from fretes.models import Frete
from motoristas.models import Motorista

class ChecklistOperacional(models.Model):
    frete = models.OneToOneField(Frete, on_delete=models.CASCADE, related_name='checklist')
    documentos_motorista = models.BooleanField(default=False)
    risco_aprovado = models.BooleanField(default=False)
    coleta_confirmada = models.BooleanField(default=False)
    comprovante_coleta = models.BooleanField(default=False)
    em_transito_confirmado = models.BooleanField(default=False)
    descarga_confirmada = models.BooleanField(default=False)
    comprovante_descarga = models.BooleanField(default=False)
    financeiro_conferido = models.BooleanField(default=False)
    ocorrencias_pendentes = models.BooleanField(default=False)
    atualizado_em = models.DateTimeField(auto_now=True)

    @property
    def percentual(self):
        campos = [
            self.documentos_motorista, self.risco_aprovado, self.coleta_confirmada,
            self.comprovante_coleta, self.em_transito_confirmado, self.descarga_confirmada,
            self.comprovante_descarga, self.financeiro_conferido,
        ]
        return int((sum(1 for c in campos if c) / len(campos)) * 100)

    def __str__(self):
        return f'Checklist #{self.frete_id} - {self.percentual}%'

class HistoricoStatusFrete(models.Model):
    frete = models.ForeignKey(Frete, on_delete=models.CASCADE, related_name='historico_status')
    status_anterior = models.CharField(max_length=30, blank=True)
    status_novo = models.CharField(max_length=30)
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.frete_id}: {self.status_anterior} -> {self.status_novo}'

class ConsultaRisco(models.Model):
    class Status(models.TextChoices):
        PENDENTE='PENDENTE','Pendente'
        APROVADO='APROVADO','Aprovado'
        REPROVADO='REPROVADO','Reprovado'
        BLOQUEADO='BLOQUEADO','Bloqueado'
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, related_name='consultas_risco')
    frete = models.ForeignKey(Frete, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas_risco')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    protocolo = models.CharField(max_length=80, blank=True)
    observacao = models.TextField(blank=True)
    payload = models.JSONField(default=dict, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.motorista} - {self.status}'

class DocumentoFrete(models.Model):
    class Tipo(models.TextChoices):
        CTE='CTE','CT-e'
        NFE='NFE','NF-e'
        COMPROVANTE_COLETA='COMPROVANTE_COLETA','Comprovante de coleta'
        COMPROVANTE_DESCARGA='COMPROVANTE_DESCARGA','Comprovante de descarga'
        OUTRO='OUTRO','Outro'
    frete = models.ForeignKey(Frete, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=40, choices=Tipo.choices, default=Tipo.OUTRO)
    numero = models.CharField(max_length=80, blank=True)
    arquivo_url = models.URLField(blank=True)
    descricao = models.TextField(blank=True)
    validado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.tipo} - Frete #{self.frete_id}'

class OcorrenciaOperacional(models.Model):
    class Gravidade(models.TextChoices):
        BAIXA='BAIXA','Baixa'
        MEDIA='MEDIA','Média'
        ALTA='ALTA','Alta'
        CRITICA='CRITICA','Crítica'
    class Status(models.TextChoices):
        ABERTA='ABERTA','Aberta'
        EM_TRATATIVA='EM_TRATATIVA','Em tratativa'
        RESOLVIDA='RESOLVIDA','Resolvida'
        CANCELADA='CANCELADA','Cancelada'
    frete = models.ForeignKey(Frete, on_delete=models.CASCADE, related_name='ocorrencias')
    titulo = models.CharField(max_length=160)
    descricao = models.TextField()
    gravidade = models.CharField(max_length=20, choices=Gravidade.choices, default=Gravidade.MEDIA)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA)
    responsavel = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    resolvido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.titulo} - {self.status}'

class TarefaOperacional(models.Model):
    frete = models.ForeignKey(Frete, on_delete=models.CASCADE, related_name='tarefas')
    titulo = models.CharField(max_length=160)
    descricao = models.TextField(blank=True)
    prazo = models.DateTimeField(null=True, blank=True)
    concluida = models.BooleanField(default=False)
    responsavel = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['concluida', 'prazo', '-criado_em']

    def __str__(self):
        return self.titulo
