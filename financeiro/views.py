from django.shortcuts import render
from django.http import HttpResponse
from financeiro.models import Perfil, Receita, DespesaFixa, DespesaVariavel, Metas
from financeiro.funcoes.comum import OperacoesUsuarios
from django.shortcuts import render, redirect
import json



def inserirValor(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "InserirSaldo.html")
        else:
            infos = json.loads(request.body)
            tipo = infos.get("tipo","").strip()
            valor = int(infos.get("valor","").strip())
            nome = infos.get("nome","").strip()
            data = infos.get("data","").strip()
            descricao = infos.get("descricao","").strip()

            id_user = request.user.id
            perfil = Perfil.objects.get(fk_user=id_user)

            if tipo == "receita":
                Receita.objects.create(perfil= perfil,valor=valor,data=data ,descricao=descricao)
            elif tipo == "despesa_fixa":
                DespesaFixa.objects.create(perfil=perfil,valor=valor,data=data,descricao=descricao)
            elif tipo == "despesa_variavel":
                DespesaVariavel.objects.create(perfil=perfil,valor=valor,data=data,descricao=descricao)
            elif tipo == "meta":
                Metas.objects.create(perfil=perfil,nome=nome,valor=valor,data=data,descricao=descricao)
            return redirect('home')
    else:
        return redirect('home')

def displaySaldo(request):
    if request.user.is_authenticated:
        print("id user: ",request.user.id)
        print("id perfil_user", Perfil.objects.get(fk_user=request.user.id))
        operacoes = OperacoesUsuarios(request.user.id)
        saldo = operacoes.calcular_saldo()
        receita = operacoes.total_valor("Receita")
        despesafixa = operacoes.total_valor("DespesaFixa")
        despesavariavel = operacoes.total_valor("DespesaVariavel")
        valores = {
            "saldo": saldo,
            "receita": receita,
            "despesa_fixa": despesafixa,
            "despesa_variavel": despesavariavel
        }

        return render(request, "SaldoDisplay.html",valores)