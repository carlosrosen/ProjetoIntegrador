from datetime import date

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from decimal import Decimal

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("O username deve ser preenchido")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # só chama save 1 vez
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter is_superuser=True.')
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    saldoAtual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    dataUltimaTransacaoVerificada = models.DateField(default=date.today())

    def operarSaldoAtual(self, valor:Decimal, tipo:str, inversor:bool = False):
        valor = abs(valor)
        if inversor == True:
            valor = -valor
        if tipo == 'R':
            self.saldoAtual += valor
        elif tipo == 'D':
            self.saldoAtual -= valor
        self.save()

    def __str__(self):
        return f'''
        {str(self.id)} - {self.username} - {self.email} - {str(self.saldoAtual)}
        '''
