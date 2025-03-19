from django.shortcuts import render
from django.http import HttpResponse
from financeiro.models import Perfil
from ProjetoIntegrador.financeiro.funcoes import saldo

#
def mostrar_saldo(request):
    saldo = saldo.calcular_saldo(Perfil)
    HttpResponse(saldo)