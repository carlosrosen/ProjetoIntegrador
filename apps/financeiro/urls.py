from django.urls import path
from . import views
from .views import *

app_name = 'financeiro'

# As URLs de Login e Cadastro
urlpatterns = [
    path('criarReceita/', views.criarTransacaoReceita, name='criar-receita'),
    path('criarDespesa/', views.criarTransacaoDespesa, name='criar-despesa'),
    path("editar-transacao/<int:parcela_id>", views.editarTransacaoUnica, name='editar-transacao'),
    path("editar-transacao-parcelada-/<int:parcela_id>", views.editarTransacaoParcelada, name='editar-parcela'),
    path("deletar-transacao/<int:parcela_id>", views.deletarParcela, name='deletar-transacao'),
]