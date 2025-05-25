from django.contrib import admin
from .models import Metas, Objetivos, TransacaoObjetivo
# Register your models here.

admin.site.register(Metas)
admin.site.register(Objetivos)
admin.site.register(TransacaoObjetivo)
