from datetime import date
from idlelib.rpc import request_queue

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from apps.financeiro.models import Categoria
from django.urls import reverse
from datetime import date

from apps.financeiro.models import HistoricoSaldo

from apps.usuarios.models import CustomUser

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
        user = CustomUser.objects.filter(Q(username=usuario) | Q(email=email)).first()
        if user:
            messages.error(request, 'Já existe um usuário com esse nome de usuário ou email')
            return redirect(reverse('usuario:cadastro'))
        
        # Chamando a função de criar usuário do Django
        user = CustomUser.objects.create_user(username=usuario, email=email, password=senha)

        user.dataUltimaTransacaoVerificada(date.today())
        user.save()

        #Logando o usuario automaticamente e redicionando para a aplicação
        login(request, user)
        HistoricoSaldo.inicializarPrimeiroValor(user)
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

def configuraçoes(request):
    user = request.user

    if not user.is_authenticated:
        return redirect(reverse('core:index'))

    context = {
        'mes': date.today().month
        , 'ano': date.today().year
        , 'usuario': user
    }

    if not request.method == "POST":
        return render(request, 'configuraçoes.html', context)

    if "atualizar_perfil" in request.POST:
        novo_usuario = request.POST.get('usuario', '').strip()
        novo_email = request.POST.get('email', '').strip()

        pode_salvar = True

        if user.username != novo_usuario:
            if CustomUser.objects.filter(username__iexac=novo_usuario).exists():
                pode_salvar = False

        if user.email != novo_email:
            if CustomUser.objects.filter(email__iexact=novo_email).exists():
                pode_salvar = False

        if pode_salvar:
            user.username = novo_usuario
            user.email = novo_email
            user.save()
            # Mensagem de foi atualizado com sucesso as informações novas do usuario
            return render(request, 'configuraçoes.html', context)

    elif "confirmar_senha" in request.POST:
        senha_atual = request.POST.get('senha', '').strip()
        nova_senha = request.POST.get('nova_senha', '').strip()
        confirmar_senha = request.POST.get('confirmar_senha', '').strip()

        if not user.check_password(senha_atual):
            return # Mensagem de erro

        if not nova_senha or not confirmar_senha:
            return # Mensagem de erro

        if nova_senha != confirmar_senha:
            return # Mensagem de erro

        else:
            user.set_password(nova_senha)
            user.save()
            update_session_auth_hash(request, user)
            # Colocar uma mensagem de troca de senha concluida
            return redirect(reverse('usuario:configuracoes'))

    elif "deletar_conta" in request.POST:
        deslogar(user)
        user.delete()
        # Mensagem que a conta foi deletada com sucesso
        return redirect(reverse('core:index'))





