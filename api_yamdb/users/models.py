from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Пользователи.
    """

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('user', 'User'),
        ('moderator', 'Moderator')
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
    )
    email = models.EmailField(
        'Email',
        max_length=254,
        blank=False,
        unique=True,
        verbose_name='Адрес эл.почты',
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Права доступа относительно статуса пользователя',
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        """Метаданные."""
        verbose_name_plural = 'Пользователи'
        verbous_name = 'Пользователь'
        ordering = ('id',)

    def __str__(self):
        return str(self.username)
