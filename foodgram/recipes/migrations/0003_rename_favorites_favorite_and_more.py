# Generated by Django 4.1.5 on 2023-02-05 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Favorites",
            new_name="Favorite",
        ),
        migrations.RenameModel(
            old_name="RecipeIngredients",
            new_name="RecipeIngredient",
        ),
        migrations.RemoveConstraint(
            model_name="shoppingcart",
            name="user_recipe_shoppinglist",
        ),
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(upload_to="uploads/", verbose_name="Изображение"),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopping_carts",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopping_carts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddConstraint(
            model_name="shoppingcart",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="user_recipe_shopping_cart"
            ),
        ),
    ]
