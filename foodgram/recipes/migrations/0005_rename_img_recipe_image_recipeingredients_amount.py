# Generated by Django 4.1.5 on 2023-01-18 13:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0004_alter_recipe_ingredients_alter_recipe_tags_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recipe",
            old_name="img",
            new_name="image",
        ),
        migrations.AddField(
            model_name="recipeingredients",
            name="amount",
            field=models.PositiveSmallIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(
                        1, "Должно быть целое число, большее 0"
                    )
                ],
                verbose_name="Количество",
            ),
        ),
    ]