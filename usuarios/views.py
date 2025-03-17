from django.http.response import  HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

#Função para cadastrar Usuarios
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        #Filtra se já existe um e-mail parecido no banco de dados, para evitar cadastro repetido
        user = User.objects.filter(email=email).first()

        #Caso o e-mail exista exibira uma mensagem
        if user:
            return HttpResponse('Já existe um usuário com esse e-mail')

        # Chamando a função de criar usuário do Django
        user = User.objects.create_user(username=usuario, email=email, password=senha)

        # Salva as informações do usuario no banco de dados
        user.save()

        return HttpResponse("Usuário cadastrado com sucesso!")

#Função de requisitar o site de Login
def login(request):
    return render(request, 'login.html')

#Função de requisitar o site de EsqueciMinhaSenha
def esqueci(request):
    return render(request, 'esqueci.html')