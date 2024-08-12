# Generated by Django 4.2.14 on 2024-08-11 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('cover', models.CharField(max_length=100)),
                ('author', models.TextField()),
                ('actor', models.TextField()),
                ('story', models.TextField()),
                ('genre', models.TextField()),
                ('rating', models.DecimalField(decimal_places=2, max_digits=4)),
                ('release_date', models.DateField()),
            ],
        ),
    ]
