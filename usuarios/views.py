from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse

#Função para cadastrar novos usuarios
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        usuario = request.POST.get('usuario', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '')

        #Filtra se já existe um e-mail ou usuario parecidos no banco de dados, para evitar cadastros repetidos.
        user = User.objects.filter(Q(username=usuario) | Q(email=email)).first()

        #Caso o e-mail ou usuario exista
        if user:
            return HttpResponse('Já existe um usuário com esse usuário ou email')

        # Chamando a função de criar usuário do Django
        user = User.objects.create_user(username=usuario, email=email, password=senha)

        return HttpResponse("Usuário cadastrado com sucesso!")

#Função de Login
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        usuario = request.POST.get('usuario', '').strip()
        senha = request.POST.get('senha')

        #Autentica se o email e a senha são compativeís
        user = authenticate(username=usuario, password=senha)

        if user:
            return HttpResponse("Usuário logado com sucesso!")
        else:
            return HttpResponse("Usuário ou senha errada")

#Função de requisitar o site de EsqueciMinhaSenha
def esqueci(request):
    return render(request, 'esqueci.html')