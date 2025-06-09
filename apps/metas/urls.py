from django.urls import path
from django.urls import reverse_lazy
from . import views

app_name = 'metas'

urlpatterns = [
    path('', views.menuMetas, name='meta'),
    path('criar-meta/', views.criarMeta, name='criar-meta'),
    path('editar-meta/<int:meta_id>/', views.editarMeta, name='editar-meta'),
    path('deletar-meta/<int:meta_id>/', views.deletarMeta, name='deletar-meta'),
]