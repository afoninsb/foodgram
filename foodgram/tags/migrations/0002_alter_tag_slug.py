# Generated by Django 4.1.5 on 2023-02-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(max_length=200, unique=True, verbose_name="Слаг"),
        ),
    ]
