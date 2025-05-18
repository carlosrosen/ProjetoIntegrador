from django.urls import path
from . import views

app_name = 'financeiro'

# As URLs de Login e Cadastro
urlpatterns = [
    path('', views.Transacao, name='Transacao'),
]