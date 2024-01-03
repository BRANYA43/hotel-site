from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from accounts.manager import UserManager


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, verbose_name="Ім'я")
    last_name = models.CharField(max_length=255, null=True, verbose_name='Прізвище')
    birthday = models.DateField(null=True, verbose_name='Дата народження')
    telephone = models.CharField(max_length=20, null=True, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Профіль Користувача'
        verbose_name_plural = 'Профілі Користувачів'

    @property
    def has_necessary_data(self):
        return all([self.first_name, self.last_name, self.birthday, self.telephone])


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name='Електронна пошта')
    password = models.CharField(max_length=20, verbose_name='Пароль')
    email_is_confirmed = models.BooleanField(default=False, verbose_name='Електронна пошта підтверджена')
    is_active = models.BooleanField(default=True, verbose_name='Активний')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал готелю')
    joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата приєднання')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
