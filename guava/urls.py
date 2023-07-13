from django.urls import path
from . import views

urlpatterns = [
    path('mitra/', views.mitra,name='mitra'),
    path('mitra/createmitra', views.create_mitra,name='createmitra'),
    # path('mitra/updatemitra/<str:id>', views.update_mitra,name='updatemitra'),
    # path('deletemitra/<str:id>', views.delete_mitra,name='deletemitra'),

]