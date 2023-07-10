from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )

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
