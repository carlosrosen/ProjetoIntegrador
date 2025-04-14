from django.urls import path
from django.contrib.auth import views as auth_views # Importei essa biblioteca para utilizar as views do Django de auth
from . import views

app_name = 'usuario'

# As URLs de Login e Cadastro
urlpatterns = [
    path('cadastro/', views.cadastrar, name='cadastro'),
    path('login/', views.logar, name='login'),
    path('logout/', views.deslogar, name='logout'),
    path('resetar-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('resetar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('resetar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('resetar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

