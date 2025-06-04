from django.urls import path, include
from apps.core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/transacoes/', include('apps.financeiro.urls')),
    path('dashboard/objetivo/', include('apps.objetivos.urls')),
    path('dashboard/meta', include('apps.metas.urls')),
    path('notfound/', views.notfound, name='erro404'),
    path('dashboard/erro/<str:mensagem>', views.erro, name='erro')
]