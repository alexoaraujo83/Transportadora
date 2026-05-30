from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='EventoSeguranca', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('tipo',models.CharField(choices=[('LOGIN_FALHA','Falha de login'),('RATE_LIMIT','Rate limit'),('ACESSO_NEGADO','Acesso negado'),('WEBHOOK_INVALIDO','Webhook inválido'),('ACAO_CRITICA','Ação crítica'),('SISTEMA','Sistema')],max_length=40)),('severidade',models.CharField(choices=[('BAIXA','Baixa'),('MEDIA','Média'),('ALTA','Alta'),('CRITICA','Crítica')],default='MEDIA',max_length=20)),('ip',models.GenericIPAddressField(blank=True,null=True)),('caminho',models.CharField(blank=True,max_length=255)),('metodo',models.CharField(blank=True,max_length=10)),('detalhe',models.TextField(blank=True)),('metadados',models.JSONField(blank=True,default=dict)),('criado_em',models.DateTimeField(db_index=True,default=django.utils.timezone.now)),('usuario',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,to=settings.AUTH_USER_MODEL))], options={'ordering':['-criado_em']}),
        migrations.CreateModel(name='PoliticaAcesso', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('perfil',models.CharField(db_index=True,max_length=40)),('modulo',models.CharField(max_length=80)),('pode_visualizar',models.BooleanField(default=True)),('pode_criar',models.BooleanField(default=False)),('pode_editar',models.BooleanField(default=False)),('pode_excluir',models.BooleanField(default=False)),('pode_exportar',models.BooleanField(default=False)),('ativo',models.BooleanField(default=True)),('atualizado_em',models.DateTimeField(auto_now=True))], options={'unique_together':{('perfil','modulo')}}),
        migrations.AddIndex(model_name='eventoseguranca', index=models.Index(fields=['tipo','severidade','criado_em'], name='seguranca_e_tipo_8b72e6_idx')),
    ]
