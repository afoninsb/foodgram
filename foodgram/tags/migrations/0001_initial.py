# Generated by Django 4.1.5 on 2023-02-04 13:57

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        max_length=7,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^#([A-Fa-f0-9]{6})$",
                                message="Код цвета должен быть в 16-ричном формате: #FFFFFF",
                            )
                        ],
                        verbose_name="Цвет",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                        verbose_name="Слаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тэг",
                "verbose_name_plural": "Тэги",
                "ordering": ("name",),
            },
        ),
    ]
