from django.urls import path
from . import views

urlpatterns = [
    # LOGIN
    path('home',views.home, name="home"),
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

]