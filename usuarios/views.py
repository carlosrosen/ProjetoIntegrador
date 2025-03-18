from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

#Função para cadastrar novos usuarios
def cadastrar(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        usuario = request.POST.get('usuario', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '')

        #Filtra se já existe um e-mail ou usuario parecidos no banco de dados, para evitar cadastros repetidos.
        user = User.objects.filter(Q(username=usuario) | Q(email=email)).first()
        if user:
            messages.error(request, 'Já existe um usuário com esse nome de usuário ou email')
            return redirect('cadastro')

        # Chamando a função de criar usuário do Django
        user = User.objects.create_user(username=usuario, email=email, password=senha)
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')

#Função de Login
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        usuario = request.POST.get('usuario', '').strip()
        senha = request.POST.get('senha')

        #Autentica se o email e a senha são compativeís
        user = authenticate(request, username=usuario, password=senha)

        if user:
            login(request, user)
            return HttpResponse("Usuário logado com sucesso!")
        else:
            messages.error(request, 'Usuário ou senha errada')
            redirect('login')

#W.I.P
#Função de requisitar o site de EsqueciMinhaSenha
def esqueci(request):
    return render(request, 'esqueci.html')