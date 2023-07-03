from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator)
from django.db import models

from .validators import validate_username, validate_year


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Represents a user of the application.
    Inherits fields like username, first_name, last_name, email, password from AbstractUser.
    Adds additional field: role.
    Provides properties to check user roles: is_guest, is_author, is_admin.
    """

    ROLE_GUEST = 'user'
    ROLE_AUTHOR = 'author'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = (
        (ROLE_GUEST, 'Guest'),
        (ROLE_AUTHOR, 'Authorized user'),
        (ROLE_ADMIN, 'Administrator'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_GUEST,
        verbose_name='Role',
    )

    @property
    def is_guest(self):
        return self.role == self.ROLE_GUEST

    @property
    def is_author(self):
        return self.role == self.ROLE_AUTHOR

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Subscriber',
        related_name='subscriber',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author',
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscribe'),
            models.CheckConstraint(check=~models.Q(user=models.F('author')),
                                   name='no_self_subscribe')
        ]

        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self) -> str:
        return f'{self.user} subscribe to {self.author}'
