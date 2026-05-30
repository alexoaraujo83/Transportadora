from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import TokenExterno

@api_view(['GET'])
@permission_classes([AllowAny])
def consulta_publica_api(request, token):
    try:
        t=TokenExterno.objects.select_related('frete').get(token=token, ativo=True)
    except TokenExterno.DoesNotExist:
        return Response({'detail':'Token inválido ou inativo.'}, status=404)
    f=t.frete
    return Response({'id':f.id,'origem':f.origem,'destino':f.destino,'carga':f.carga,'status':f.status,'data_coleta':f.data_coleta})
urlpatterns=[path('consulta/<str:token>/', consulta_publica_api, name='api_portal_consulta')]
