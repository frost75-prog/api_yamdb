from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('user', 'User'),
        ('moderator', 'Moderator')
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField('Email', blank=False, unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default='user')

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
