# Generated manually for Fusion Cargas Inteligente V10
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fretes','0001_initial'),
        ('motoristas','0001_initial'),
        ('financeiro','0002_campos_gestao'),
    ]
    operations = [
        migrations.CreateModel(name='ContaFinanceira', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('nome', models.CharField(max_length=120)),('tipo', models.CharField(choices=[('CAIXA','Caixa'),('BANCO','Banco'),('CARTEIRA','Carteira digital')], default='BANCO', max_length=20)),
            ('banco', models.CharField(blank=True, max_length=80)),('agencia', models.CharField(blank=True, max_length=30)),('conta', models.CharField(blank=True, max_length=40)),
            ('saldo_inicial', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('ativa', models.BooleanField(default=True)),('criada_em', models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name='ContaPagarReceber', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('natureza', models.CharField(choices=[('PAGAR','Conta a pagar'),('RECEBER','Conta a receber')], max_length=20)),
            ('descricao', models.CharField(max_length=180)),('documento', models.CharField(blank=True, max_length=80)),('favorecido', models.CharField(blank=True, max_length=140)),
            ('valor_original', models.DecimalField(decimal_places=2, max_digits=12)),('valor_pago', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('vencimento', models.DateField()),('data_baixa', models.DateField(blank=True, null=True)),
            ('status', models.CharField(choices=[('ABERTA','Aberta'),('PARCIAL','Parcial'),('BAIXADA','Baixada'),('VENCIDA','Vencida'),('CANCELADA','Cancelada')], default='ABERTA', max_length=20)),
            ('categoria', models.CharField(blank=True, max_length=80)),('centro_custo', models.CharField(blank=True, max_length=80)),('observacao', models.TextField(blank=True)),('criado_em', models.DateTimeField(auto_now_add=True)),('atualizado_em', models.DateTimeField(auto_now=True)),
            ('conta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financeiro.contafinanceira')),('frete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contas_financeiras', to='fretes.frete')),
        ]),
        migrations.CreateModel(name='RepasseMotorista', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('valor_frete', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('pedagio', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('adiantamento', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('descontos', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('saldo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('status', models.CharField(choices=[('PENDENTE','Pendente'),('PROGRAMADO','Programado'),('PAGO','Pago'),('CANCELADO','Cancelado')], default='PENDENTE', max_length=20)),('data_programada', models.DateField(blank=True, null=True)),('data_pagamento', models.DateField(blank=True, null=True)),('observacao', models.TextField(blank=True)),('criado_em', models.DateTimeField(auto_now_add=True)),('atualizado_em', models.DateTimeField(auto_now=True)),
            ('frete', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='repasse_motorista', to='fretes.frete')),('motorista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='motoristas.motorista')),
        ]),
        migrations.CreateModel(name='ComissaoOperacional', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('base_calculo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('percentual', models.DecimalField(decimal_places=2, default=0, max_digits=5)),('valor', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('status', models.CharField(choices=[('PENDENTE','Pendente'),('APROVADA','Aprovada'),('PAGA','Paga'),('CANCELADA','Cancelada')], default='PENDENTE', max_length=20)),('data_pagamento', models.DateField(blank=True, null=True)),('observacao', models.TextField(blank=True)),('criado_em', models.DateTimeField(auto_now_add=True)),
            ('frete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comissoes', to='fretes.frete')),('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='ConciliacaoBancaria', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('data_movimento', models.DateField()),('historico', models.CharField(max_length=200)),('valor', models.DecimalField(decimal_places=2, max_digits=12)),('documento', models.CharField(blank=True, max_length=80)),('status', models.CharField(choices=[('PENDENTE','Pendente'),('CONCILIADA','Conciliada'),('DIVERGENTE','Divergente')], default='PENDENTE', max_length=20)),('observacao', models.TextField(blank=True)),('criado_em', models.DateTimeField(auto_now_add=True)),
            ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conciliacoes', to='financeiro.contafinanceira')),('lancamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financeiro.contapagarreceber')),
        ]),
        migrations.CreateModel(name='FechamentoFinanceiro', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('competencia', models.CharField(help_text='AAAA-MM', max_length=7)),('receitas', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('despesas', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('lucro_bruto', models.DecimalField(decimal_places=2, default=0, max_digits=12)),('margem_percentual', models.DecimalField(decimal_places=2, default=0, max_digits=7)),('observacao', models.TextField(blank=True)),('criado_em', models.DateTimeField(auto_now_add=True)),('fechado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
        ], options={'unique_together': {('competencia',)}}),
    ]
