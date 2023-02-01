from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(verbose_name='Название', max_length=200)
    text = models.TextField(verbose_name='Текст')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredients',
    )
    tags = models.ManyToManyField(Tag, verbose_name='Тэги')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления(мин)',
        validators=(
            MinValueValidator(1, 'Должно быть целое число, большее 0'),
        )
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=''
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Модель: вхождение ингредиентов в рецепты."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipe_ingrdient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='recipe_ingrdient'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(1, 'Должно быть целое число, большее 0'), ),
        default=1
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='recipe_ingredient'
            ),
        )
        verbose_name = 'Ингредиенты в рецептах'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Favorites(models.Model):
    """Модель рецептов-фаворитов пользователей."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_recipe_favorites'
            ),
        )


class ShoppingCart(models.Model):
    """Модель рецептов на закупку."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shoppinglist'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shoppinglist'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_recipe_shoppinglist'
            ),
        )
        verbose_name = 'Лист покупок'
        verbose_name_plural = 'Листы покупок'
