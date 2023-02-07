from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        validators=(
            RegexValidator(
                '^#([A-Fa-f0-9]{6})$',
                message='Код цвета должен быть в 16-ричном формате: #FFFFFF'
            ),
        )
    )
    slug = models.SlugField(verbose_name='Слаг', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name
