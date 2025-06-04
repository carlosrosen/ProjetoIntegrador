from django.urls import path
from django.urls import reverse_lazy
from . import views

app_name = 'metas'

urlpatterns = [
    path('', views.menuMetas, name='meta'),
    path('editar-meta/', views.editarMeta, name='editar-meta'),
    path('deletar-meta/', views.deletarMeta, name='deletar-meta/'),
]