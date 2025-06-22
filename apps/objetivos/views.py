from datetime import date

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.utils import timezone

from decimal import Decimal

from apps.financeiro.models import Categoria
from apps.objetivos.dominio.pausar import Pausar
from apps.objetivos.dominio.tipoobjetivo import TipoObjetivo
from apps.objetivos.dominio.valorobjetivo import ValorObjetivo
from apps.objetivos.models import Objetivos
from apps.objetivos.operacoes.objetivos import GetObjetivo, OperacoesObjetivo

from common.dominio.data import Data

def menuObjetivos(request):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    getterobjetivos = GetObjetivo(request.user.id)
    objetivos = getterobjetivos.todosEmOrdem()

    categorias = Categoria.objects.all()

    context = {'objetivos': objetivos
             , 'categorias': categorias
             , 'todas_categorias_receita': categorias.filter(tipo='R')
             , 'todas_categorias_despesa': categorias.filter(tipo='D')
             , 'hoje': date.today()
             , 'mes': date.today().month
             , 'ano': date.today().year
    }
    return render(request, 'objetivos.html', context)

def detalheObjetivo(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    objetivo = get_object_or_404(Objetivos, id=id)

    # Caso seja outro usuario tentando acessar um objetivo que não lhe pertence
    if objetivo.user_fk != request.user:
        return

    getter = GetObjetivo(request.user.id)
    datas, valores = getter.variacao(id)
    categorias = Categoria.objects.all()
    context = {'objetivo': objetivo
        , 'valoresHistorico': valores
        , 'datas': datas
        , 'mes': date.today().month
        , 'ano': date.today().year
        , 'categorias': categorias
        , 'todas_categorias_receita': categorias.filter(tipo='R')
        , 'todas_categorias_despesa': categorias.filter(tipo='D')
        , 'hoje': date.today()
        }

    return render(request, 'objetivo-detalhes.html', context)


def criarObjetivo(request):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    if not request.method == 'POST':
        return redirect(reverse('core:dashboard'))

    operacoes = OperacoesObjetivo(request.user.id)

    titulo = request.POST.get('tituloObjetivo')
    valor_desejado = ValorObjetivo(request.POST.get('valorDesejado'))
    valor_guardado  = ValorObjetivo(request.POST.get('valorGuardado'))
    data_fim = Data(request.POST.get('anoFinal'))

    operacoes.criar(titulo, valor_desejado, valor_guardado, data_fim)

    url = request.POST.get('next') or reverse('core:dashboard')
    return redirect(url)



def editarObj(request, objetivo_id):
    if request.method == 'POST':
        nova_data = Data(request.POST.get('novaData'))
        titulo = request.POST.get('novoTitulo')
        valor = Decimal(request.POST.get('novoValor'))
        objetivo = get_object_or_404(Objetivos, id=objetivo_id, user_fk__id=request.user.id)
        pausado = Pausar(request.POST.get('pausar'))

        operacao = OperacoesObjetivo(request.user.id)
        operacao.editar(objetivo, titulo, valor, nova_data, pausado.valor)

        return redirect('core:objetivos:detalhe_objetivo', id=objetivo_id)

def deletarObj(request, objetivo_id):
    if request.method == 'POST':
        objetivo = get_object_or_404(Objetivos, id=objetivo_id, user_fk__id=request.user.id)
        operacao = OperacoesObjetivo(request.user.id)
        operacao.deletar(objetivo)
        return redirect('core:objetivos:menu_objetivos')

def depositarObj(request, objetivo_id):
    if request.method == 'POST':
        data_atual = timezone.now().date()
        valor = Decimal(request.POST.get('valorDeposito'))
        objetivo = get_object_or_404(Objetivos, id=objetivo_id, user_fk__id=request.user.id)

        operacao = OperacoesObjetivo(request.user.id)
        operacao.deposito(objetivo, valor, data_atual) # Arrumar aqui

        return redirect('core:objetivos:detalhe_objetivo', id=objetivo_id)

def resgatarObj(request, objetivo_id):
    if request.method == 'POST':
        data_atual = timezone.now().date()
        valor = Decimal(request.POST.get('valorResgate'))
        objetivo = get_object_or_404(Objetivos, id=objetivo_id, user_fk__id=request.user.id)

        operacao = OperacoesObjetivo(request.user.id)
        operacao.resgate(objetivo, valor, data_atual) # Arrumar aqui

        return redirect('core:objetivos:detalhe_objetivo', id=objetivo_id)

