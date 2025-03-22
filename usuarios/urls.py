from django.urls import path
from . import views

app_name = 'usuario'

# As URLs de Login e Cadastro
urlpatterns = [
    path('cadastro/', views.cadastrar, name='cadastro'),
    path('login/', views.logar, name='login'),
    path('logout/', views.deslogar, name='logout'),
    path('esqueci/', views.esqueci, name='esqueci')
]

