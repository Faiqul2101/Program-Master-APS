# Generated by Django 4.1.6 on 2023-07-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guava', '0005_alter_mitra_status_mitra'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detail_penjualan',
            old_name='kuantitas',
            new_name='kuantitas_komoditas',
        ),
        migrations.AddField(
            model_name='detail_penjualan',
            name='kuantitas_produk',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
