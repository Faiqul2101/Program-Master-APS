from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.mitra)
admin.site.register(models.panen)
admin.site.register(models.detail_panen)
admin.site.register(models.komoditas)
admin.site.register(models.grade)
admin.site.register(models.detail_penjualan)
admin.site.register(models.penjualan)
admin.site.register(models.produk)
admin.site.register(models.pasar)
admin.site.register(models.transaksi_lain)
