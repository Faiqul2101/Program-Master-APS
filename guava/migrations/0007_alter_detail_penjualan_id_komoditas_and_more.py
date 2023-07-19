# Generated by Django 4.1.6 on 2023-07-17 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guava', '0006_rename_kuantitas_detail_penjualan_kuantitas_komoditas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_penjualan',
            name='id_komoditas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='guava.komoditas'),
        ),
        migrations.AlterField(
            model_name='detail_penjualan',
            name='id_produk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='guava.produk'),
        ),
        migrations.AlterField(
            model_name='detail_penjualan',
            name='kuantitas_komoditas',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='detail_penjualan',
            name='kuantitas_produk',
            field=models.PositiveIntegerField(null=True),
        ),
    ]