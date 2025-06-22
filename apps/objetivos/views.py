from django.shortcuts import render, reverse, redirect, get_object_or_404

from apps.objetivos.models import Objetivos
from apps.objetivos.operacoes.objetivos import GetObjetivo


def menuObjetivos(request):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    getterobjetivos = GetObjetivo(request.user.id)
    objetivos = getterobjetivos.todosEmOrdem()
    context = {'objetivos': objetivos}
    return render(request, 'objetivos.html', context)

def detalheObjetivo(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    objetivo = get_object_or_404(Objetivos, id=id)

    # Caso seja outro usuario tentando acessar um objetivo que não lhe pertence
    if objetivo.user_fk != request.user:
        return

    return render(request, 'objetivo-detalhes.html')


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

