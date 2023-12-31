from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('home',views.home, name="home"),

    # LOGIN
    path('',views.loginview, name='login'),
    path('performlogin',views.performlogin,name="performlogin"),
    path('performlogout',views.performlogout,name="performlogout"),

    # MITRA
    path('mitra/', views.mitra,name='mitra'),
    path('mitra/createmitra', views.create_mitra,name='createmitra'),
    path('mitra/updatemitra/<str:id>', views.update_mitra,name='updatemitra'),
    path('mitra/validasimitra/<str:id>', views.validasi_mitra,name='validasimitra'),
    path('deletemitra/<str:id>', views.delete_mitra,name='deletemitra'),

    # GRADE
    path('grade/', views.grade,name='grade'),
    path('grade/creategrade', views.create_grade,name='creategrade'),
    path('grade/updategrade/<int:id>', views.update_grade,name='updategrade'),
    path('grade/deletegrade/<int:id>', views.delete_grade,name='deletegrade'),

    # PRODUK
    path('produk/', views.produk,name='produk'),
    path('produk/createproduk', views.create_produk,name='createproduk'),
    path('produk/updateproduk/<str:id>', views.update_produk,name='updateproduk'),
    path('deleteproduk/<str:id>', views.delete_produk,name='deleteproduk'),

    # PASAR
    path('pasar/', views.pasar,name='pasar'),
    path('pasar/createpasar', views.create_pasar,name='createpasar'),
    path('pasar/updatepasar/<str:id>', views.update_pasar,name='updatepasar'),
    path('deletepasar/<str:id>', views.delete_pasar,name='deletepasar'),

    # KOMODITAS
    path('komoditas/', views.komoditas,name='komoditas'),
    path('komoditas/createkomoditas', views.create_komoditas,name='createkomoditas'),
    path('komoditas/updatekomoditas/<str:id>', views.update_komoditas,name='updatekomoditas'),
    path('deletekomoditas/<str:id>', views.delete_komoditas,name='deletekomoditas'),

    # TRANSAKSI LAIN
    path('transaksilain/', views.transaksi_lain,name='transaksilain'),
    path('transaksilain/createtransaksilain', views.create_transaksi_lain,name='createtransaksilain'),
    path('transaksilain/updatetransaksilain/<str:id>', views.update_transaksi_lain,name='updatetransaksilain'),
    path('deletetransaksilain/<str:id>', views.delete_transaksi_lain,name='deletetransaksilain'),

    # PANEN
    path('panen/', views.panen,name='panen'),
    path('panen/updatepanen/<str:id>', views.update_panen,name='updatepanen'),
    path('deletepanen/<str:id>', views.delete_panen,name='deletepanen'),

    # DETAIL PANEN
    path('detailpanen/', views.detailpanen,name='detailpanen'),
    path('panen/createpanen/<str:id>/', views.create_panen,name='createpanen'),
    path('detailpanen/ubahdetailpanen/<str:id>/', views.ubah_panen,name='ubahdetailpanen'),
    path('detailpanen/updatedetailpanen/<str:id>', views.update_detailpanen,name='updatedetailpanen'),
    path('deletedetailpanen/<str:id>', views.delete_detailpanen,name='deletedetailpanen'),

    # PENJUALAN
    path('penjualan/', views.penjualan,name='penjualan'),
    path('penjualan/createpenjualan', views.cerate_penjualan,name='createpenjualan'),
    path('penjualan/updatepenjualan/<str:id>', views.updatepenjualan,name='updatepenjualan'),
    path('deletepenjualan/<str:id>', views.deletepenjualan,name='deletepenjualan'),

    # DETAIL PENJUALAN
    path('detailpenjualan', views.detail_penjualan,name='detailpenjualan'),
    path('detailpenjualan1', views.detail_penjualan_komoditas,name='detailpenjualan_komoditas'),
    path('detailpenjualan2', views.detail_penjualan_produk,name='detailpenjualan_produk'),
    path('detailpenjualan/createdetailpenjualan_produk/<int:id>/', views.create_detailpenjualan_produk, name='createdetailpenjualan_produk'),
    path('detailpenjualan/createdetailpenjualan_komoditas/<int:id>/', views.create_detailpenjualan_komoditas, name='createdetailpenjualan_komoditas'),
    path('detailpenjualan/updatedetailpenjualan/<str:id>', views.update_detailpenjualan,name='updatedetailpenjualan'),
    path('deletedetailpenjualan/<str:id>', views.delete_detailpenjualan,name='deletedetailpenjualan'),
    # LAPORAN
    path('laporan', views.laporan_laba_rugi, name='laporan'),
    path('laporanpdf/<str:mulai>/<str:akhir>',views.laporan_laba_rugi_pdf,name='laporanpdf'),
    path('laporanjual', views.laporanpenjualan, name='laporanjual'),
    path('laporanpenjualanpdf/<str:mulai>/<str:akhir>',views.laporanpenjualanpdf,name='laporanpenjualanpdf'),
    path('laporanpanen', views.laporanpanen,name='laporanpanen'),
    path('laporanpanenpdf/<str:mulai>/<str:akhir>',views.laporanpanenpdf,name='laporanpanenpdf'),



    ]   