from django.contrib.auth.models import AbstractUser
from django.db import models

LIMIT_USERNAME = 150


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=LIMIT_USERNAME,
        unique=True,
        help_text='Уникальное имя пользователя для входа в систему.'
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        help_text='Уникальный адрес электронной почты пользователя.'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=LIMIT_USERNAME,
        help_text='Имя пользователя.'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=LIMIT_USERNAME,
        help_text='Фамилия пользователя.'
    )

    def __str__(self):
        return self.username
