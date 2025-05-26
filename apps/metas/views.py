from django.shortcuts import render, reverse, redirect


def criarMeta(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

def editarMeta(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

def deletarMeta(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
