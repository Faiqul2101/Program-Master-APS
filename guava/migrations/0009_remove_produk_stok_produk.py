# Generated by Django 4.1.6 on 2023-07-23 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guava', '0008_produk_stok_produk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produk',
            name='stok_produk',
        ),
    ]
