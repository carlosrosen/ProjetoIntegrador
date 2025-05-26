from django.urls import path, include
from apps.core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/transacoes/', include('apps.financeiro.urls')),
    path('objetivo/', include('apps.objetivos.urls')),
    path('notfound/', views.notfound, name='erro404'),
]