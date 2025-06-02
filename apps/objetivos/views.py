from django.shortcuts import render, reverse, redirect

from apps.objetivos.models import Objetivos
from apps.objetivos.operacoes.objetivos import GetObjetivo


def menuObjetivos(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    objetivos = GetObjetivo.todosEmOrdem(request.user.id)
    return render(request, 'objetivos.html', objetivos)

def criarObj(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

def editarObj(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

def deletarObj(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

def depositarObj(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

def resgatarObj(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

