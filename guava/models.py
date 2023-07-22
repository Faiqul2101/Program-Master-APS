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
    status_mitra = models.BooleanField(default=None, null=True)

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
    
class produk(models.Model):
    id_produk = models.AutoField(primary_key=True)
    namaproduk = models.CharField(max_length=15)
    satuanproduk = models.CharField(max_length=15)
    hargaproduk = models.IntegerField()
    stok_produk = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.namaproduk)

    # def get_stok_tersedia_produk(self):
    #     total_terjual = sum(detail_penjualan_obj.kuantitas_produk for detail_penjualan_obj in self.detail_penjualan_set.all())
    #     self.stok_produk -= total_terjual
    #     return self.stok_produk

class komoditas(models.Model):
    id_komoditas = models.AutoField(primary_key=True)
    id_grade = models.ForeignKey(grade, on_delete=models.CASCADE)
    nama_komoditas = models.CharField(max_length=50)
    harga_beli = models.IntegerField()
    harga_jual = models.IntegerField()

    def __str__(self):
        return "{} - {}".format(self.nama_komoditas, self.id_grade)
    
    def get_stok_tersedia(self):
        total_stok = sum(detail_panen_obj.jumlah for detail_panen_obj in self.detail_panen_set.all())
        total_terjual = sum(detail_penjualan_obj.kuantitas_komoditas for detail_penjualan_obj in self.detail_penjualan_set.all())
        stok_tersedia = total_stok - total_terjual if total_stok >= total_terjual else 0
        return stok_tersedia
    
    def kurangi_stok(self, jumlah_dikurangi):
        stok_tersedia = self.get_stok_tersedia()
        if stok_tersedia >= jumlah_dikurangi:
            self.total_stok -= jumlah_dikurangi
            self.save()
class detail_panen(models.Model):
    id_detailpanen = models.AutoField(primary_key=True)
    id_panen = models.ForeignKey(panen, on_delete=models.CASCADE)
    id_komoditas = models.ForeignKey(komoditas, on_delete=models.CASCADE)
    jumlah = models.PositiveBigIntegerField()
    tanggalkadaluwarsa = models.DateField()

    def __str__(self):
        return str(self.id_panen)
    
    def get_total_stok(self):
        return self.jumlah
    


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
    id_produk = models.ForeignKey(produk,null=True, on_delete=models.CASCADE)
    id_komoditas = models.ForeignKey(komoditas,null=True, on_delete=models.CASCADE)
    kuantitas_produk = models.PositiveIntegerField(null=True,)
    kuantitas_komoditas = models.PositiveIntegerField(null=True,)

    def __str__(self):
        return str(self.id_penjualan)
    
    def get_total_terjual(self):
        return self.kuantitas_komoditas
    
class transaksi_lain(models.Model):
    id_transaksi = models.AutoField(primary_key=True)
    jenis_transaksi = models.CharField(max_length=50)
    tanggal_transaksi = models.DateField()
    biaya = models.IntegerField()

    def __str__(self):
        return str(self.id_transaksi)




