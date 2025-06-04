from django.shortcuts import render, reverse, redirect

from apps.metas.operacoes.metas import GetMetas


def menuMetas(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    gettermetas= GetMetas(request.user.id)
    metas = gettermetas.todosEmOrdem()
    context = {'metas': metas}
    return render(request, 'metas.html', context)

def criarMeta(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

def editarMeta(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

def deletarMeta(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
