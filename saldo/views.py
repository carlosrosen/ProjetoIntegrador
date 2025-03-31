from django.shortcuts import render
from django.http import HttpResponse
from .models import Metas, Transacao, Categoria
#from ProjetoIntegrador.saldo.funcoes.comum import OperacoesUsuarios
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
import json

def inserirSaldo(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    # verifica se o metodo da pagina é GET para pegar as informações
    if request.method == 'GET':
        #alem de mostrar o template inserirSaldo.html é enviado as categorias existentes para o usuario fazer as suas inserções
        return render(request, 'inserirSaldo.html', {'Categorias': list(Categoria.objects.all())})
    
    # As informações estão sendo retornadas em tipo JSON, então ela converte o formato JSON para um dicionario em python
    infos = json.loads(request.body.decode('utf-8'))
    
    # Faz as verificações de qual categoria salvar e salva as informações formatadas em sua respectiva categoria
    if infos.get('salvar').strip().lower() == 'categoria':
        nome = infos.get('nome','').strip().lower()
        nome = nome[0].upper() + nome[1:]
        tipo = infos.get('tipo','').strip()
        Categoria.objects.create(nome=nome, tipo=tipo)
        
    elif infos.get('salvar').strip().lower() == 'transacao':
        valor = infos.get('valor','').strip()
        data = infos.get('data','').strip()
        tipo = infos.get('tipo','').strip()
        categoria_id = infos.get('categoria_id','').strip()
        categoria = Categoria.objects.get(id=categoria_id)
        eh_recorrente = infos.get('eh_recorrente','')
        quantidade = infos.get('quantidade','').strip()
        descricao = infos.get('descricao','').strip()
        Transacao.objects.create(
            user_fk=request.user,
            categoria_fk = categoria,
            tipo=tipo,
            valor=valor,
            data=data,
            eh_recorrente=eh_recorrente,
            status = True,
            descricao=descricao
        )

    elif infos.get('salvar').strip().lower() == 'meta':
        nome = infos.get('nome','').strip()
        valor = infos.get('valor','').strip()
        data_inicio = infos.get('data_inicio','').strip()
        data_fim = infos.get('data_fim','').strip()
        descricao = infos.get('descricao','').strip()
        Metas.objects.create(
            user_fk = request.user,
            nome=nome,
            valor=valor,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
    return redirect(reverse('saldo:inserir-saldo'))
        
def editarSaldo(request, transacao_id):
    # Verifica a autenticação
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'GET':
        return render(request,'editarSaldo.html',
            {'transacao': Transacao.objects.get(id=transacao_id,user_fk= request.user),
            'categorias': Categoria.objects.all()}
        )
    acao = request.POST.get('ativar_botao')
    print('\n\n',acao,'\n\n')
    transacao = Transacao.objects.get(id = transacao_id, user_fk= request.user)
    if acao == 'apagar':
        transacao.delete()
        return redirect(reverse('saldo:historico-saldo'))
    if acao == 'editar':
        transacao.categoria_fk = Categoria.objects.get(id= request.POST['categoria'])
        transacao.tipo = request.POST['tipo']
        transacao.valor = request.POST['valor']
        transacao.data = request.POST['data']
        transacao.descricao = request.POST['descricao'].strip()
        transacao.status = request.POST['status']
        transacao.save()
        messages.success(request, 'Salvo com sucesso')
        return redirect(reverse('saldo:historico-saldo'))

def historicoSaldo(request):
    # Verifica a autenticação
    if not request.user.is_authenticated:
        return redirect('home')
    
    #chama todos os objetos
    transacoes = Transacao.objects.filter(user_fk= request.user)
    categorias = Categoria.objects.all()
    
    #com base nos filtros colocado no site, armazena os filtros
    tipo = request.GET.get('tipo', '')
    categoria_id = request.GET.get('categoria', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    valor_min = request.GET.get('valor_min', '')
    
    # Faz a filtragem de cada atributo
    if tipo:
        transacoes = transacoes.filter(tipo=tipo)

    if categoria_id:
        transacoes = transacoes.filter(categoria_fk_id=categoria_id)

    if data_inicio:
        transacoes = transacoes.filter(data__gte=data_inicio)

    if data_fim:
        transacoes = transacoes.filter(data__lte=data_fim)

    if valor_min:
        transacoes = transacoes.filter(valor__gte=valor_min)
    
    # Caarrega o site e envia as informações com ou sem filtros para serem mostrados
    return render(request, 'historicoSaldo.html', {
        'transacoes': transacoes,
        'categorias': categorias
        }
    )