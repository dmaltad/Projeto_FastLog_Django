# seu_app/urls.py

from django.urls import path
from . import views # Supondo que suas views estão no mesmo app

urlpatterns = [
    # URLs para LISTAR e CRIAR
    # A página principal agora será a lista de todos, que também conterá o formulário de criação.
    path('', views.entregadores, {'status': 'todos'}, name='entregadores'),
    path('ativos/', views.entregadores, {'status': 'ativo'}, name='entregadores_ativos'),
    path('inativos/', views.entregadores, {'status': 'inativo'}, name='entregadores_inativos'),

    # URLs para ações em um entregador ESPECÍFICO
    # Usamos <int:pk> para capturar o ID do entregador na URL
    path('<int:pk>/', views.entregadores_detalhes, name='entregadores_detalhes'),
    path('<int:pk>/editar/', views.entregador_update, name='entregador_update'),
    path('<int:pk>/remover/', views.entregador_delete, name='entregador_delete'),
]