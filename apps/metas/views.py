from django.shortcuts import render, reverse, redirect, get_object_or_404
from decimal import Decimal
from datetime import date
from unicodedata import category

from apps.metas.operacoes.metas import GetMetas, OperacoesMeta, Metas
from apps.financeiro.models import Categoria
from common.dominio.data import Data


def menuMetas(request):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    gettermetas= GetMetas(request.user.id)
    metas = gettermetas.todosEmOrdem()
    context = {'metas': metas
               ,'categorias': Categoria.GetTodasCategorias()
               ,'mes': date.today().month
               ,'ano': date.today().year
    }
    return render(request, 'metas.html', context)

def criarMeta(request):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    if not request.method == "POST":
        return redirect(request.session['ultima_url'])
    operacoes_meta = OperacoesMeta(request.user.id)
    valor = request.POST.get('valor')
    tipo = request.POST.get('tipo')
    data_inicio = request.POST.get('data_inicio')
    data_fim = request.POST.get('data_fim')
    descricao = request.POST.get('descricao')
    categoria = request.POST.get('categoria')
    Categoria.verificacaoNomesCategoria(categoria)
    categoria = Categoria.objects.get(nome=categoria)

    print(valor,'\n',tipo,'\n',descricao,'\n',categoria,'\n', data_inicio,'\n', data_fim)

    operacoes_meta.criarMeta(categoria=categoria
                             , valor= Decimal(valor)
                             , tipo=tipo
                             , data_inicio= Data(data_inicio)
                             , data_fim= Data(data_fim)
                             , descricao=descricao
    )
    return redirect(request.session['ultima_url'])

def editarMeta(request, meta_id):
    if request.method == 'POST':
        print(request.POST)
        meta = get_object_or_404(Metas, id=meta_id)
        categoria = request.POST.get('categoria')
        tipo = request.POST.get('tipoMeta')
        valor = Decimal(request.POST.get('valor'))
        data_inicio = Data(request.POST.get('data_inicio'))
        data_fim = Data(request.POST.get('data_fim'))
        descricao = request.POST.get('descricao')

        categoria = Categoria.objects.get(nome=categoria)
        print(categoria)

        operacao = OperacoesMeta(request.user.id)
        operacao.editarMeta(meta, categoria, tipo, valor, data_inicio, data_fim, descricao)

    return redirect("core:metas:meta")

def deletarMeta(request, meta_id):
    if request.method == 'POST':
        meta = get_object_or_404(Metas, id=meta_id)
        operacao = OperacoesMeta(request.user.id)
        operacao.deletarMeta(meta)
        return redirect("core:metas:meta")
