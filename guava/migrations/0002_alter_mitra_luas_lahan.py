# Generated by Django 4.1.6 on 2023-07-13 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guava', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mitra',
            name='luas_lahan',
            field=models.PositiveIntegerField(null=True),
        ),
    ]