from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from api_yamdb.settings import MAX_LENGTH_USERNAME
from .validators import validate_username


class UserRole(models.TextChoices):
    """ Роли пользователей. """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


MAX_LENGTH_ROLES = max(len(_) for _ in UserRole.choices[1])


class UserManagerSuperuserIsAdmin(UserManager):
    """
    Кастомный менеджер для создания суперюзера с правами админа.
    """
    def create_superuser(
            self, username, email, password, role=UserRole.ADMIN,
            **extra_fields):
        return super().create_superuser(
            username, email, password, role=UserRole.ADMIN, **extra_fields)


class User(AbstractUser):
    """
    Модель для User. Параметры полей.
    """
    username = models.CharField(
        verbose_name='Имя пользователя',
        validators=[validate_username],
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        db_index=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_LENGTH_ROLES,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    objects = UserManagerSuperuserIsAdmin()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        """
        Свойство.
        Возвращает права админа.
        """
        return self.role == UserRole.ADMIN

    @property
    def is_moderator(self):
        """
        Свойство.
        Возвращает права модератора.
        """
        return self.role == UserRole.MODERATOR
