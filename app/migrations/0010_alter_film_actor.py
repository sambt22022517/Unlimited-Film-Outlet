# Generated by Django 4.2.14 on 2024-08-17 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_film_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='actor',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
