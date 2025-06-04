from django.urls import path
from . import views
from .views import *

app_name = 'financeiro'

# As URLs de Login e Cadastro
urlpatterns = [
    path('criarReceita/', views.criarTransacaoReceita, name='CriarTransacao'),
    path('criarDespesa/', views.criarTransacaoDespesa, name='CriarDespesa'),
]
