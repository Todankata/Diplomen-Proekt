# Generated by Django 3.1 on 2023-04-22 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_favorites'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorites',
        ),
    ]
