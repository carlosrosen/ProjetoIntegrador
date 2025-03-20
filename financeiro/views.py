from django.shortcuts import render
from django.http import HttpResponse
from financeiro.models import Perfil, Receita, DespesaFixa, DespesaVariavel, Metas
from financeiro.funcoes.comum import calcular_saldo
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
                receita = Receita.objects.create(perfil= perfil,valor=valor,data=data ,descricao=descricao)
            return redirect('home')
    else:
        return redirect('home')
