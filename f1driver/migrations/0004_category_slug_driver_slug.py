# Generated by Django 4.0.3 on 2022-04-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('f1driver', '0003_alter_category_options_alter_driver_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='driver',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique=True, verbose_name='URL'),
        ),
    ]