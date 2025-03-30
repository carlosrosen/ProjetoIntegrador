from django.shortcuts import render
from django.http import HttpResponse
from .models import Metas, Transacao, Categoria
#from ProjetoIntegrador.saldo.funcoes.comum import OperacoesUsuarios
from django.shortcuts import render, redirect
from django.urls import reverse
import json

def inserirValor(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'GET':
        return render(request, 'inserirSaldo.html', {'Categorias': list(Categoria.objects.filter())})
    
    infos = json.loads(request.body)
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
        categoria = Categoria.objects.get(id= categoria_id)
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
    return redirect(reverse('saldo:alterar-saldo'))
        
        

'''def mostrarSaldo(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    print('id user: ',request.user.id)
    print('id perfil_user', Perfil.objects.get(fk_user=request.user.id))
    operacoes = OperacoesUsuarios(request.user.id)
    saldo = operacoes.calcular_saldo()
    receita = operacoes.total_valor('Receita')
    despesafixa = operacoes.total_valor('DespesaFixa')
    despesavariavel = operacoes.total_valor('DespesaVariavel')
    valores = {
        'saldo': saldo,
        'receita': receita,
        'despesa_fixa': despesafixa,
        'despesa_variavel': despesavariavel
    }
    
    return render(request, 'SaldoDisplay.html',valores)
'''
