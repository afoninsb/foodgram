# Generated by Django 4.1.5 on 2023-01-17 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0001_initial"),
        ("ingredients", "0001_initial"),
        ("recipes", "0003_alter_favorites_user_alter_shoppinglist_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                through="recipes.RecipeIngredients",
                to="ingredients.ingredient",
                verbose_name="Ингредиенты",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                through="recipes.RecipeTags", to="tags.tag", verbose_name="Тэги"
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredients",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="recipe_ingrdient",
                to="ingredients.ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AlterField(
            model_name="recipetags",
            name="tag",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="recipe_tag",
                to="tags.tag",
                verbose_name="Тэг",
            ),
        ),
        migrations.DeleteModel(
            name="Ingredient",
        ),
        migrations.DeleteModel(
            name="Tag",
        ),
    ]