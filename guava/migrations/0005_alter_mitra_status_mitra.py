# Generated by Django 4.1.6 on 2023-07-13 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guava', '0004_alter_mitra_status_mitra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mitra',
            name='status_mitra',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
