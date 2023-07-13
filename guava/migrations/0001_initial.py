# Generated by Django 4.1.6 on 2023-07-13 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='grade',
            fields=[
                ('id_grade', models.AutoField(primary_key=True, serialize=False)),
                ('nama_grade', models.CharField(max_length=15)),
                ('deskripsi', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='mitra',
            fields=[
                ('id_mitra', models.AutoField(primary_key=True, serialize=False)),
                ('nama_mitra', models.CharField(max_length=30)),
                ('alamat_mitra', models.TextField(blank=True, null=True)),
                ('nomor_mitra', models.PositiveIntegerField()),
                ('tanggal_mulai_mitra', models.DateField()),
                ('durasi_kontrak', models.PositiveIntegerField()),
                ('luas_lahan', models.PositiveIntegerField()),
                ('status_mitra', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='pasar',
            fields=[
                ('id_pasar', models.AutoField(primary_key=True, serialize=False)),
                ('nama_pasar', models.CharField(max_length=50)),
                ('alamat_pasar', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='produk',
            fields=[
                ('id_produk', models.AutoField(primary_key=True, serialize=False)),
                ('namaproduk', models.CharField(max_length=15)),
                ('satuanproduk', models.CharField(max_length=15)),
                ('hargaproduk', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='transaksi_lain',
            fields=[
                ('id_transaksi', models.AutoField(primary_key=True, serialize=False)),
                ('jenis_transaksi', models.CharField(max_length=50)),
                ('tanggal_transaksi', models.DateField()),
                ('biaya', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='penjualan',
            fields=[
                ('id_penjualan', models.AutoField(primary_key=True, serialize=False)),
                ('tanggal_penjualan', models.DateField()),
                ('id_pasar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guava.pasar')),
            ],
        ),
        migrations.CreateModel(
            name='panen',
            fields=[
                ('id_panen', models.AutoField(primary_key=True, serialize=False)),
                ('tanggal_panen', models.DateField()),
                ('id_mitra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guava.mitra')),
            ],
        ),
        migrations.CreateModel(
            name='komoditas',
            fields=[
                ('id_komoditas', models.AutoField(primary_key=True, serialize=False)),
                ('nama_komoditas', models.CharField(max_length=50)),
                ('harga_beli', models.IntegerField()),
                ('harga_jual', models.IntegerField()),
                ('id_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guava.grade')),
            ],
        ),
        migrations.CreateModel(
            name='detail_penjualan',
            fields=[
                ('id_detailpenjualan', models.AutoField(primary_key=True, serialize=False)),
                ('kuantitas', models.PositiveIntegerField()),
                ('id_komoditas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guava.komoditas')),
                ('id_penjualan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guava.penjualan')),
                ('id_produk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guava.produk')),
            ],
        ),
        migrations.CreateModel(
            name='detail_panen',
            fields=[
                ('id_detailpanen', models.AutoField(primary_key=True, serialize=False)),
                ('jumlah', models.PositiveBigIntegerField()),
                ('tanggalkadaluwarsa', models.DateField()),
                ('id_komoditas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guava.komoditas')),
                ('id_panen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guava.panen')),
            ],
        ),
    ]
