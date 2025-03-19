from django.shortcuts import render
from django.http import HttpResponse
from financeiro.models import Perfil, Receita, DespesaFixa, DespesaVariavel, Metas
from financeiro.funcoes import comum
import json


def inserirValor(request):
    if request.method == "GET":
        return render(request, "inserirsaldo.html")
    infos = json.loads(request.body)
    tipo = infos.get("tipo","").strip()
    valor = infos.get("valor","").strip()
    nome = infos.get("nome","").strip()
    data = infos.get("data","").strip()
    descricao = infos.get("descricao","").strip()

    if tipo == "Receita":
        aux = Receita(valor=valor, data=data,descricao=descricao)
        aux.save()






    
    
    
    