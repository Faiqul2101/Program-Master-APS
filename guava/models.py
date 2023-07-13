from django.db import models

# Create your models here.
class mitra(models.Model):
    id_mitra = models.AutoField(primary_key=True)
    nama_mitra = models.CharField(max_length=30)
    alamat_mitra = models.TextField(blank=True, null=True)
    nomor_mitra = models.PositiveIntegerField()
    tanggal_mulai_mitra = models.DateField()
    durasi_kontrak = models.PositiveIntegerField()
    luas_lahan = models.PositiveIntegerField(null=True)
    status_mitra = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nama_mitra)
    
class panen(models.Model):
    id_panen = models.AutoField(primary_key=True)
    id_mitra = models.ForeignKey(mitra, on_delete=models.CASCADE)
    tanggal_panen= models.DateField()

    def __str__(self):
        return str(self.id_mitra)

class grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    nama_grade = models.CharField(max_length=15)
    deskripsi = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nama_grade)

class komoditas(models.Model):
    id_komoditas = models.AutoField(primary_key=True)
    id_grade = models.ForeignKey(grade, on_delete=models.CASCADE)
    nama_komoditas = models.CharField(max_length=50)
    harga_beli = models.IntegerField()
    harga_jual = models.IntegerField()

    def __str__(self):
        return str(self.nama_komoditas)

class detail_panen(models.Model):
    id_detailpanen = models.AutoField(primary_key=True)
    id_panen = models.ForeignKey(panen, on_delete=models.CASCADE)
    id_komoditas = models.ForeignKey(komoditas, on_delete=models.CASCADE)
    jumlah = models.PositiveBigIntegerField()
    tanggalkadaluwarsa = models.DateField()

    def __str__(self):
        return str(self.id_panen)
    
class produk(models.Model):
    id_produk = models.AutoField(primary_key=True)
    namaproduk = models.CharField(max_length=15)
    satuanproduk = models.CharField(max_length=15)
    hargaproduk = models.IntegerField()

    def __str__(self):
        return str(self.namaproduk)

class pasar(models.Model):
    id_pasar = models.AutoField(primary_key=True)
    nama_pasar = models.CharField(max_length=50)
    alamat_pasar =models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.nama_pasar)
    
class penjualan(models.Model):
    id_penjualan = models.AutoField(primary_key=True)
    id_pasar = models.ForeignKey(pasar, on_delete=models.CASCADE)
    tanggal_penjualan = models.DateField()

    def __str__(self):
        return str(self.id_pasar)

class detail_penjualan(models.Model):
    id_detailpenjualan = models.AutoField(primary_key=True)
    id_penjualan = models.ForeignKey(penjualan, on_delete=models.CASCADE)
    id_produk = models.ForeignKey(produk, on_delete=models.CASCADE)
    id_komoditas = models.ForeignKey(komoditas, on_delete=models.CASCADE)
    kuantitas = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id_penjualan)
    
class transaksi_lain(models.Model):
    id_transaksi = models.AutoField(primary_key=True)
    jenis_transaksi = models.CharField(max_length=50)
    tanggal_transaksi = models.DateField()
    biaya = models.IntegerField()

    def __str__(self):
        return str(self.id_transaksi)




