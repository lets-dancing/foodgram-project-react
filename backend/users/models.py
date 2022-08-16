from django.contrib.auth.models import AbstractUser
from django.db import models


class User (AbstractUser):
    email = models.EmailField(
        max_length=150,
        db_index=True,
        unique=True,
        verbose_name='Пользовательский email'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name='Короткое имя',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'username'

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
