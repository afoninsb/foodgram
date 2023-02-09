from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


class User(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    email = models.EmailField(verbose_name='email', max_length=254)
    password = models.CharField(verbose_name='Пароль', max_length=150)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки пользователей на авторов."""

    subscriber = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscription_subscriber'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='subscription_author'
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('subscriber', 'author'),
                name='uniqe_subscriber_author'
            ),
            CheckConstraint(
                check=~Q(author=F('subscriber')),
                name='subscriber_not_author',
            )
        )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
