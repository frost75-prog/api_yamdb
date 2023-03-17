from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from api_yamdb.settings import REGEX_USER


def username_not_correct(value):
    return not REGEX_USER.match(value) or value.lower() == 'me'


class MyUserManager(UserManager):

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательно!')
        if username_not_correct(username):
            raise ValueError('Invalid username!')
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):

    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True
    )
    bio = models.TextField('Biography', blank=True, null=True)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default='user')
    objects = MyUserManager()

    REQUIRED_FIELDS = ('email', 'password')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == self.ROLE_CHOICES[2][0]

    @property
    def is_moderator(self):
        return self.role == self.ROLE_CHOICES[1][0]
