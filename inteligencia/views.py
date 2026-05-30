from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import InsightOperacional, PrevisaoFrete, ScoreMotorista
from .services import InteligenciaOperacionalService

@login_required
def painel_inteligencia(request):
    if request.method=='POST':
        criados=InteligenciaOperacionalService.gerar_insights()
        messages.success(request, f'Análise concluída. Insights verificados/criados: {len(criados)}.')
        return redirect('painel_inteligencia')
    ctx={
        'kpis':InteligenciaOperacionalService.kpis_inteligencia(),
        'insights':InsightOperacional.objects.filter(resolvido=False).order_by('-criado_em')[:50],
        'previsoes':PrevisaoFrete.objects.select_related('frete').order_by('-atualizado_em')[:30],
        'scores':ScoreMotorista.objects.select_related('motorista').order_by('-score')[:20],
    }
    return render(request,'inteligencia/painel.html',ctx)
