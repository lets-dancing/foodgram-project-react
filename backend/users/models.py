from django.contrib.auth.models import AbstractUser
from django.db import models


class User (AbstractUser):
    email = models.EmailField(
        max_length=254,
        db_index=True,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.email

# from django.contrib.auth import get_user_model
# from django.db import models

# User = get_user_model()


# class Follow(models.Model):
#     """Модель для подписки на автора"""
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='follower',
#         verbose_name='Подписчик'
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='following',
#         verbose_name='Автор'
#     )

#     class Meta:
#         verbose_name = 'Подписка'
#         verbose_name_plural = 'Подписки'
#         ordering = ('id',)
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'author'],
#                 name='unique_follow'
#             )
#         ]

#     def __str__(self):
#         return f'Подписчик {self.user} - автор {self.author}'
