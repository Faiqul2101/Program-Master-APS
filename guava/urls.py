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
    path('panen/createpanen/<str:id>/', views.create_panen,name='createpanen'),
    path('detailpanen/', views.detailpanen,name='detailpanen'),
    path('detailpanen/ubahdetailpanen/<str:id>/', views.ubah_panen,name='ubahdetailpanen'),
    # path('detailpanen/createdetailpanen/<int:id>/', views.create_detailpanen,name='createdetailpanen'),
    
    # PENJUALAN
    path('penjualan/', views.penjualan,name='penjualan'),
    path('penjualan/createpenjualan', views.jual,name='createpenjualan'),
    
    # DETAIL PENJUALAN
    path('detailpenjualan1', views.detail_penjualan_komoditas,name='detailpenjualan_komoditas'),
    path('detailpenjualan2', views.detail_penjualan_produk,name='detailpenjualan_produk'),
    # path('createdetailpenjualan/<int:id>/', views.create_detailpenjualan, name='createdetailpenjualan'),
    path('detailpenjualan/createdetailpenjualan_produk/<int:id>/', views.create_detailpenjualan_produk, name='createdetailpenjualan_produk'),
    path('detailpenjualan/createdetailpenjualan_komoditas/<int:id>/', views.create_detailpenjualan_komoditas, name='createdetailpenjualan_komoditas'),

    ]