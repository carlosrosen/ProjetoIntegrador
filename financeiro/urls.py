from django.urls import path
from . import views

# As URLs de Login e Cadastro
urlpatterns = [
    path('alterar-saldo/', views.inserirValor, name='inserirValor'),
]