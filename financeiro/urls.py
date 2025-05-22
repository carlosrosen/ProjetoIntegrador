from django.urls import path
from . import views
from .views import EditarTransacao

app_name = 'financeiro'

# As URLs de Login e Cadastro
urlpatterns = [
    path('cr', views.CriarTransacao, name='Transacao'),
    path('ed', views.EditarTransacao, name='ed'),
    path('deltodas',views.deletarTodasParcelas, name='deletarTodasParcelas'),
    path('deluma', views.deletarUmaParcela, name='deletarUmaParcela'),
]