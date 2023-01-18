from django.core.validators import validate_slug
from django.db import models


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        null=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True,
        validators=(validate_slug, ),
        null=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name
