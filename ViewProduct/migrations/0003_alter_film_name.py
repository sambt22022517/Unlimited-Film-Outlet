# Generated by Django 4.2.14 on 2024-08-11 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ViewProduct', '0002_actor_author_genre_remove_film_actor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
