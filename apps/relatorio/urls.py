from django.urls import path
from django.urls import reverse_lazy
from apps.relatorio import views

app_name = 'relatorio'

urlpatterns = [
   path('mensal/', views.relatorioMensal, name='relatorio_mensal'),
]