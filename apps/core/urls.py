from django.urls import path, include
from apps.core import views
from apps.financeiro.views import menuExtrato

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transacoes/', include('apps.financeiro.urls')),
    path('objetivos/', include('apps.objetivos.urls')),
    path('meta/', include('apps.metas.urls')),
    path('extrato/<int:mes>/<int:ano>/', menuExtrato, name='menuExtrato'),
    path('relatorio/', include('apps.relatorio.urls'), name='relatorio'),
    path('notfound/', views.notfound, name='erro404'),
    path('erro/<str:mensagem>', views.erro, name='erro')
]