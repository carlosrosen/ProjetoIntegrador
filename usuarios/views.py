from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from saldo.models import Categoria
from django.urls import reverse

#Função para cadastrar novos usuarios
def cadastrar(request):
    if request.user.is_authenticated:
        return redirect(reverse('core:index'))
    
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        # Armazenando as informações fornecidas para a criação do usuario
        usuario = request.POST.get('usuario', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()
        repetir_senha = request.POST.get('repetir_senha', '').strip()
        
        # Confirmação de senha
        if senha != repetir_senha:
            messages.error(request, 'As senhas não coincidem. Tente novamente.')
            return redirect(reverse('usuario:cadastro'))
        
        # Filtra se já existe um e-mail ou usuario parecidos no banco de dados, para evitar cadastros repetidos.
        user = User.objects.filter(Q(username=usuario) | Q(email=email)).first()
        if user:
            messages.error(request, 'Já existe um usuário com esse nome de usuário ou email')
            return redirect(reverse('usuario:cadastro'))
        
        # Chamando a função de criar usuário do Django
        user = User.objects.create_user(username=usuario, email=email, password=senha)

        #Logando o usuario automaticamente e redicionando para a aplicação
        login(request, user)
        return redirect(reverse('core:dashboard'))

#Função de Login
def logar(request):
    if request.user.is_authenticated:
        return redirect(reverse('core:dashboard'))
        
    if request.method == "GET":
        return render(request, 'login.html')
    
    usuario = request.POST.get('usuario', '').strip()
    senha = request.POST.get('senha','').strip()

    # Autentica se o email e a senha são compativeís
    user = authenticate(request, username=usuario, password=senha)

    if user:
        login(request, user)
        return redirect(reverse('core:dashboard'))
    else:
        messages.error(request, 'Usuário ou senha errada')
        return redirect(reverse('usuario:login'))

def deslogar(request):
    logout(request)
    return redirect(reverse('core:index'))

#W.I.P
#Função de requisitar o site de EsqueciMinhaSenha
def esqueci(request):
    return render(request, 'esqueci.html')