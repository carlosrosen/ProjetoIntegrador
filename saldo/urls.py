from django.urls import path
from . import views

app_name = 'saldo'

# As URLs de Login e Cadastro
urlpatterns = [
    path('alterar-saldo', views.inserirValor, name='alterar-saldo'),
    #path('mostrar-saldo', views.mostrarSaldo, name='mostra-saldo')
]