DOKUMENTASI PROGRAM MASTER APS 


1. Deskripsi Singkat:
    - Program ini dibuat dengan tujuan untuk memudahkan pencatatan stok pada CV BumiAji dan mempermudah untuk owner dalam men-generate informasi yang dibutuhkan dalam bisnis berupa laporan rekap penjualan, panen, dan laporan laba rugi. Program ini juga dilengkapi dengan 1 Area Chart yang menggambarkan kenaikan/penurunan pada penjualan tiap bulan, serta 2 Pie Chart yang menggambarkan proporsi pasar dan komoditas serta produk yang dijual terhadap seluruh pemasukan pada CV. BumiAji. 
    - Program ini terdiri dari 10 entitas yang dapat dilihat pada models.py pada folder guava yang merupakan satu-satunya app pada project ini.

2. Instalasi:
    Untuk menjalankan program ini, sebelumnya perlu melakukan instalasi framework django dan package weasyprint melalui cmd atau terminal vscode.
    - Install django: pip install django
    - Install Weasyprint = pip install weasyprint

3. Penggunaan
    Untuk menggunakan program ini, anda bisa menjalankan perintah: 'python manage.py runserver' pada terminal. Setelah itu akan muncul address http://127.0.0.1:8000/ untuk menjalankan program secara lokal pada komputer anda.

    Penggunaan Program ini dibatasi pada 3 role utama yaitu owner, admin, dan karyawan dimana penggunaan role disini sebagai bentuk dari Authentication dan Authorization untuk membatasi hak akses stakeholder pada sistem.  