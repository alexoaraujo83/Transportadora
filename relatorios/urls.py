from django.urls import path
from .views import painel_relatorios, exportar_fretes_csv, exportar_financeiro_csv, exportar_operacional_csv, exportar_ocorrencias_csv, exportar_documentos_csv
app_name='relatorios'
urlpatterns=[
    path('', painel_relatorios, name='painel'),
    path('fretes.csv', exportar_fretes_csv, name='fretes_csv'),
    path('financeiro.csv', exportar_financeiro_csv, name='financeiro_csv'),
    path('operacional.csv', exportar_operacional_csv, name='operacional_csv'),
    path('ocorrencias.csv', exportar_ocorrencias_csv, name='ocorrencias_csv'),
    path('documentos.csv', exportar_documentos_csv, name='documentos_csv'),
]
