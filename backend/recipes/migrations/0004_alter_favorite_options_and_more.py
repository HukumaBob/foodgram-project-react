# Generated by Django 4.2.2 on 2023-07-04 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_favorite_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Favorite Recipe'},
        ),
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_favorite',
        ),
    ]