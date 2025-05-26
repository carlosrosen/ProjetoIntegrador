from django.contrib import admin
from apps.usuarios.models import CustomUser
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(User)