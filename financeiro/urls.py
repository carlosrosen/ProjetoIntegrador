from django.urls import path
from . import views

# As URLs de Login e Cadastro
urlpatterns = [
    path('alterar_saldo', views.inserirValor, name='inserirValor'),
    path('mostrarSaldo', views.displaySaldo, name='displaySaldo')   
]