from django.shortcuts import render, redirect
from . import models
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'loginsiam.html')
    else:
        mitraobj = models.mitra.objects.all()
        jumlah_mitra = mitraobj.count()
        return render(request, 'index.html', {
        'jumlah_mitra' : jumlah_mitra
    })

@login_required
def logoutview(request):
    logout(request)
    messages.info(request,"Berhasil Logout")
    return redirect('login')

def loginview(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render(request,"loginsiam.html")
    
def performlogin(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        print(request)
        username_login = request.POST['username']
        # print(username)
        password_login = request.POST['password']
        # print(username)
        userobj = authenticate(request, username=username_login,password=password_login)
        print(userobj)
        if userobj is not None:
            login(request, userobj)
            messages.success(request,"Login success")
            return redirect("mitra")
        else:
            messages.error(request,"Username atau Password salah !!!")
            return redirect("login")
        
@login_required
def performlogout(request):
    logout(request)
    print("Anda keluar")
    return redirect("login")

def mitra(request):
    mitraobj = models.mitra.objects.all()
    # is_admin = request.user.groups.filter(name='Admin').exists()
    # is_pegawai = request.user.groups.filter(name='Pegawai').exists()

    return render(request, 'mitra/mitra.html', {
        'mitraobj' : mitraobj,
    })

def create_mitra(request):
    if request.method == "GET":
        return render(request, 'mitra/createmitra.html')
    else:
        nama_mitra = request.POST["nama_mitra"]
        alamat_mitra = request.POST["alamat_mitra"]
        nomor_mitra = request.POST["nomor_mitra"]
        tanggal_mulai_mitra = request.POST["tanggal_mulai_mitra"]
        durasi_kontrak = request.POST["durasi_kontrak"]
        # luas_lahan = request.POST["luas_lahan"]

        newmitra = models.mitra(
            nama_mitra = nama_mitra,
            alamat_mitra = alamat_mitra,
            nomor_mitra = nomor_mitra,
            tanggal_mulai_mitra = tanggal_mulai_mitra,
            durasi_kontrak = durasi_kontrak,
            # luas_lahan = luas_lahan   
        )
        newmitra.save()
        return redirect('mitra')
    
def validasi_mitra(request,id):
    mitraobj = models.mitra.objects.get(id_mitra = id)
    if request.method == "GET" :
        # tanggal = datetime.strftime(mitraobj.tanggal_mulai_mitra, '%Y-%m-%d')
        return render(request, 'mitra/validasimitra.html', {
            'mitraobj' : mitraobj,
            # 'tanggal' : tanggal
        })
    else:
        luas = mitraobj.luas_lahan = request.POST['luas_lahan']
        if int(luas) >= 100:
            mitraobj.status_mitra = True
        else:
            mitraobj.status_mitra = False
        mitraobj.save()
        return redirect('mitra')

def update_mitra(request,id):
    mitraobj = models.mitra.objects.get(id_mitra = id)
    if request.method == "GET" :
        tanggal = datetime.strftime(mitraobj.tanggal_mulai_mitra, '%Y-%m-%d')
        return render(request, 'mitra/updatemitra.html', {
            'mitraobj' : mitraobj,
            'tanggal' : tanggal
        })
    else :
        mitraobj.nama_mitra = request.POST['nama_mitra']
        mitraobj.alamat_mitra = request.POST['alamat_mitra']
        mitraobj.nomor_mitra = request.POST['nomor_mitra']
        mitraobj.tanggal_mulai_mitra = request.POST['tanggal_mulai_mitra']
        mitraobj.durasi_kontrak = request.POST['durasi_kontrak']
        mitraobj.save()
        return redirect('mitra')

def delete_mitra(request,id):
    mitraobj = models.mitra.objects.get(id_mitra = id)
    mitraobj.delete()
    return redirect('mitra')

def grade(request):
    gradeobj = models.grade.objects.all()
    return render(request, 'grade/grade.html', {
        'gradeobj' : gradeobj
    })

@login_required
def produk(request):
    allprodukobj = models.produk.objects.all()

    return render (request, 'produk/produk.html',{
        'allprodukobj' : allprodukobj,
        })

@login_required
def create_produk(request):
    if request.method == "GET" :
        return render(request, 'produk/createproduk.html')
    else:
        nama_produk = request.POST['namaproduk']
        satuan_produk = request.POST['satuanproduk']
        harga_produk = request.POST['hargaproduk']

        models.produk(
            namaproduk = nama_produk,
            satuanproduk = satuan_produk,
            hargaproduk = harga_produk,
        ).save()
        return redirect('produk')

@login_required
def update_produk(request,id):
    produkobj = models.produk.objects.get(id_produk=id)
    if request.method == "GET":
        return render(request, 'produk/updateproduk.html', {
            'produkobj' : produkobj
            })
    else:
        produkobj.namaproduk = request.POST['namaproduk']
        produkobj.satuanproduk = request.POST['satuanproduk']
        produkobj.hargaproduk= request.POST['hargaproduk']
        produkobj.save()
        return redirect('produk')

@login_required
def delete_produk(request, id):
    produkobj = models.produk.objects.get(id_produk=id)
    produkobj.delete()
    return redirect('produk')