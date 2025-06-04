from django.shortcuts import render, reverse, redirect

from apps.objetivos.models import Objetivos
from apps.objetivos.operacoes.objetivos import GetObjetivo


def menuObjetivos(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    getterobjetivos = GetObjetivo(request.user.id)
    objetivos = getterobjetivos.todosEmOrdem()
    context = {'objetivos': objetivos}
    return render(request, 'objetivos.html', context)

def criarObjetivo(request):
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

