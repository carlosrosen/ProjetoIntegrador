from django.urls import path
from . import views

app_name = 'saldo'

# As URLs de Login e Cadastro
urlpatterns = [
    path('inserir-saldo', views.inserirSaldo, name='inserir-saldo'),
    path('editar-saldo/<int:transacao_id>', views.editarSaldo, name='editar-saldo'),
    path('historico-saldo', views.historicoSaldo, name='historico-saldo')
]