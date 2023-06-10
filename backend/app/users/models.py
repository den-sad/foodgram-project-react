from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True,
                                validators=[
                                    RegexValidator(
                                        regex='^[\\w.@+-]+\\Z',
                                        message='Набор символов неверный',
                                    ),
                                ])
    email = models.EmailField(max_length=254, unique=True, blank=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        ordering = ['pk']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
