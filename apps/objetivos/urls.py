from django.urls import path
from django.urls import reverse_lazy
from apps.objetivos import views

app_name = 'objetivos'

urlpatterns = [
    path('', views.menuObjetivos, name='menu_objetivos'),
    path('detalhe-objetivo/<int:id>/', views.detalheObjetivo, name='detalhe_objetivo'),
    path('criar-objetivo/', views.criarObjetivo, name='criar-objetivo'),
    path('editar-objetivo/<int:objetivo_id>/', views.editarObj, name='editar-objetivo'),
    path('deletar-objetivo/<int:objetivo_id>/', views.deletarObj, name='deletar-objetivo'),
    path('depositar-objetivo/<int:objetivo_id>/', views.depositarObj, name='depositar-objetivo'),
    path('resgatar-objetivo/<int:objetivo_id>/', views.resgatarObj, name='resgatar-objetivo'),
]
