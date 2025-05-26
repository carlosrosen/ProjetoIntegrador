from django.shortcuts import render, reverse, redirect

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

