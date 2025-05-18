from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/',views.dashboard ,name='dashboard'),
    path('dashboard/transacoes/', include('financeiro.urls')),
    path('manutencao/', views.manutencao, name='manutencao'),
]