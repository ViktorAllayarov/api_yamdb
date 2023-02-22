from django.contrib.auth.models import AbstractUser
from django.db import models

class RoleChoices(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    "Класс переопределяет и расширяет стандартную модель User."

    username = models.TextField(
        blank=False,
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
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )
