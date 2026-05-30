from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from fretes.models import Frete
from .models import InsightOperacional, PrevisaoFrete, ScoreMotorista
from .services import InteligenciaOperacionalService

@api_view(['GET'])
def kpis(request):
    return Response(InteligenciaOperacionalService.kpis_inteligencia())

@api_view(['POST'])
def gerar_insights(request):
    criados=InteligenciaOperacionalService.gerar_insights()
    return Response({'insights_verificados':len(criados)})

@api_view(['POST'])
def prever_frete(request, frete_id):
    try: frete=Frete.objects.get(id=frete_id)
    except Frete.DoesNotExist: return Response({'detail':'Frete não encontrado.'}, status=404)
    p=InteligenciaOperacionalService.sugerir_preco(frete)
    return Response({'frete':frete.id,'min':p.valor_sugerido_min,'ideal':p.valor_sugerido_ideal,'max':p.valor_sugerido_max,'margem':p.margem_prevista,'risco':p.risco_operacional,'explicacao':p.explicacao})

@api_view(['GET'])
def insights(request):
    data=[{'id':i.id,'tipo':i.tipo,'severidade':i.severidade,'titulo':i.titulo,'score':i.score,'frete_id':i.frete_id} for i in InsightOperacional.objects.filter(resolvido=False).order_by('-criado_em')[:100]]
    return Response(data)
urlpatterns=[path('kpis/', kpis), path('gerar-insights/', gerar_insights), path('fretes/<int:frete_id>/prever/', prever_frete), path('insights/', insights)]
