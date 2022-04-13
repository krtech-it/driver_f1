# Generated by Django 4.0.3 on 2022-04-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('f1driver', '0004_category_slug_driver_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='slug',
            field=models.SlugField(max_length=250, unique=True, verbose_name='URL'),
        ),
    ]
