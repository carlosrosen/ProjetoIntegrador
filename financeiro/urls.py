from django.urls import path
from . import views

app_name = "financeiro"

# As URLs de Login e Cadastro
urlpatterns = [
    path('alterarSaldo', views.inserirValor, name='alterarSaldo'),
    path('mostrarSaldo', views.displaySaldo, name='displaySaldo')
]