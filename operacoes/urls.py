from django.urls import path
from . import views
app_name='operacoes'
urlpatterns=[
    path('kanban/', views.kanban_fretes, name='kanban'),
    path('fretes/<int:pk>/checklist/', views.checklist_frete, name='checklist'),
    path('fretes/<int:pk>/acao/<str:acao>/', views.acao_status, name='acao_status'),
    path('risco/', views.consultas_risco, name='risco'),
    path('risco/motorista/<int:motorista_id>/', views.consultar_risco_motorista, name='consultar_risco_motorista'),
    path('risco/motorista/<int:motorista_id>/frete/<int:frete_id>/', views.consultar_risco_motorista, name='consultar_risco_motorista_frete'),
    path('documentos/', views.DocumentoListView.as_view(), name='documentos'),
    path('documentos/novo/', views.DocumentoCreateView.as_view(), name='documento_create'),
    path('documentos/<int:pk>/editar/', views.DocumentoUpdateView.as_view(), name='documento_update'),
    path('documentos/<int:pk>/excluir/', views.DocumentoDeleteView.as_view(), name='documento_delete'),
    path('ocorrencias/', views.OcorrenciaListView.as_view(), name='ocorrencias'),
    path('ocorrencias/novo/', views.OcorrenciaCreateView.as_view(), name='ocorrencia_create'),
    path('ocorrencias/<int:pk>/editar/', views.OcorrenciaUpdateView.as_view(), name='ocorrencia_update'),
    path('ocorrencias/<int:pk>/excluir/', views.OcorrenciaDeleteView.as_view(), name='ocorrencia_delete'),
    path('tarefas/', views.TarefaListView.as_view(), name='tarefas'),
    path('tarefas/novo/', views.TarefaCreateView.as_view(), name='tarefa_create'),
    path('tarefas/<int:pk>/editar/', views.TarefaUpdateView.as_view(), name='tarefa_update'),
    path('tarefas/<int:pk>/excluir/', views.TarefaDeleteView.as_view(), name='tarefa_delete'),
]
