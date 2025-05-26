from django.urls import path
from django.urls import reverse_lazy
from apps.objetivos import views

app_name = 'objetivo'

urlpatterns = [
    path('objetivo/', views.criarObj, name='objetivo'),
    path('editar-objetivo/', views.editarObj, name='editar-objetivo'),
    path('deletar-objetivo/', views.deletarObj, name='deletar-objetivo/'),
    path('depositar-objetivo/', views.depositarObj, name='depositar-objetivo/'),
    path('resgatar-objetivo/', views.resgatarObj, name='resgatar-objetivo/'),
]
