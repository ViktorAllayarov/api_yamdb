from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    "Класс переопределяет и расширяет стандартную модель User."

    username = models.TextField(
        blank=True,
        null=True,
        unique=True
    )
    email = models.EmailField(
        blank=False,
        unique=True,
    )
    first_name = models.TextField(
        blank=True,
        null=True,
    )
    last_name = models.TextField(
        blank=True,
        null=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=150,
        blank=False,
        choices=CHOICES,
        default='user',
    )
