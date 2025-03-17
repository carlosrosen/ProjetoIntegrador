from django.urls import path
from . import views

# As URLs de Login e Cadastro
urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('esqueci/', views.esqueci, name='esqueci')
]