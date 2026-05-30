from django.contrib import admin
from .models import LancamentoFinanceiro, ContaFinanceira, ContaPagarReceber, RepasseMotorista, ComissaoOperacional, ConciliacaoBancaria, FechamentoFinanceiro

@admin.register(LancamentoFinanceiro)
class LancamentoFinanceiroAdmin(admin.ModelAdmin):
    list_display=('id','tipo','descricao','valor','pago','vencimento')
    list_filter=('tipo','pago','categoria','centro_custo')
    search_fields=('descricao','categoria','centro_custo')

@admin.register(ContaFinanceira)
class ContaFinanceiraAdmin(admin.ModelAdmin):
    list_display=('nome','tipo','banco','ativa','saldo_inicial')
    list_filter=('tipo','ativa')

@admin.register(ContaPagarReceber)
class ContaPagarReceberAdmin(admin.ModelAdmin):
    list_display=('natureza','descricao','valor_original','valor_pago','saldo','vencimento','status')
    list_filter=('natureza','status','categoria','centro_custo')
    search_fields=('descricao','documento','favorecido')

@admin.register(RepasseMotorista)
class RepasseMotoristaAdmin(admin.ModelAdmin):
    list_display=('frete','motorista','valor_frete','adiantamento','descontos','saldo','status')
    list_filter=('status',)

@admin.register(ComissaoOperacional)
class ComissaoOperacionalAdmin(admin.ModelAdmin):
    list_display=('frete','usuario','base_calculo','percentual','valor','status')
    list_filter=('status',)

@admin.register(ConciliacaoBancaria)
class ConciliacaoBancariaAdmin(admin.ModelAdmin):
    list_display=('conta','data_movimento','historico','valor','status')
    list_filter=('status','conta')

@admin.register(FechamentoFinanceiro)
class FechamentoFinanceiroAdmin(admin.ModelAdmin):
    list_display=('competencia','receitas','despesas','lucro_bruto','margem_percentual','criado_em')
