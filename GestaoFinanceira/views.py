from django.shortcuts import render
from django.http import HttpResponse

def Pagina_Inicial(request):
    return render(request, "PaginaPrincipal.html")