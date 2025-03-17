from django.shortcuts import render

#Função de Cadastro
def cadastro(request):
    return render(request, 'cadastro.html')

#Função de Login
def login(request):
    return render(request, 'login.html')