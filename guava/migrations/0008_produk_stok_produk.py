# Generated by Django 4.1.6 on 2023-07-20 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guava', '0007_alter_detail_penjualan_id_komoditas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produk',
            name='stok_produk',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
