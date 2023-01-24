from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


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
            models.UniqueConstraint(
                fields=('subscriber', 'author'),
                name='subscriber_author'
            ),
        )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
