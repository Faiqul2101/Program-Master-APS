from django.shortcuts import render, redirect
from . import models
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.forms import DateInput
from django.db import transaction
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
        return redirect("mitra")
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

@login_required
def pasar(request):
    pasarobj = models.pasar.objects.all()
    # is_admin = request.user.groups.filter(name='Admin').exists()
    # is_pegawai = request.user.groups.filter(name='Pegawai').exists()

    return render(request, 'pasar/pasar.html', {
        'pasarobj' : pasarobj,
    })

@login_required
def create_pasar(request):
    if request.method == "GET":
        return render(request, 'pasar/createpasar.html')
    else:
        nama_pasar = request.POST['nama_pasar']
        alamat_pasar = request.POST['alamat_pasar']

        newpasar = models.pasar(
            nama_pasar = nama_pasar,
            alamat_pasar = alamat_pasar
        )
        newpasar.save()
        return redirect('pasar')

@login_required
def update_pasar(request,id):
    pasarobj = models.pasar.objects.get(id_pasar = id)
    if request.method == "GET" :
        return render(request, 'pasar/updatepasar.html', {
            'pasarobj' : pasarobj,
        })
    else :
        pasarobj.nama_pasar= request.POST['nama_pasar']
        pasarobj.alamat_pasar = request.POST['alamat_pasar']
        pasarobj.save()
        return redirect('pasar')

@login_required
def delete_pasar(request,id):
    pasarobj = models.pasar.objects.get(id_pasar = id)
    pasarobj.delete()
    return redirect('pasar')

def komoditas(request):
    komoditasobj = models.komoditas.objects.all()
    return render(request, 'komoditas/komoditas.html', {
        'komoditasobj' : komoditasobj
    } )

def create_komoditas(request):
    if request.method == 'GET':
        allgradeobj = models.grade.objects.all()
        allkomoditasobj = models.komoditas.objects.all()
        return render(request, 'komoditas/createkomoditas.html',{
            'datagrade' : allgradeobj,
            'datakomoditas' : allkomoditasobj})
    
    elif request.method == 'POST':
        id_grade = request.POST['id_grade']
        nama_komoditas = request.POST['nama_komoditas']
        harga_beli = request.POST['harga_beli']
        harga_jual = request.POST['harga_jual']

        # Simpan detail komoditas
        new_komoditas = models.komoditas.objects.create(
            id_grade_id = id_grade,
            nama_komoditas = nama_komoditas,
            harga_beli=harga_beli, 
            harga_jual=harga_jual
            )

        return redirect('komoditas')

def update_komoditas(request, id):
    allkomoditasobj = models.komoditas.objects.get(id_komoditas=id)
    allgradeobj = models.grade.objects.all()

    if request.method == "GET":
        return render(request, "komoditas/updatekomoditas.html", {
            'komoditasobj': allkomoditasobj,
            'datagrade': allgradeobj,
        })
    else:
        id_grade = request.POST['id_grade']
        getidgrade = models.grade.objects.get(id_grade=id_grade)
        allkomoditasobj.nama_komoditas = request.POST['nama_komoditas']
        allkomoditasobj.harga_beli = request.POST['harga_beli']
        allkomoditasobj.harga_jual = request.POST['harga_jual']
        allkomoditasobj.id_grade = getidgrade
        allkomoditasobj.save()
        return redirect('komoditas')
    
def delete_komoditas(request, id):
    komoditasobj = models.komoditas.objects.get(id_komoditas=id)
    komoditasobj.delete()
    return redirect('komoditas')

@login_required
def transaksi_lain(request):
    transaksi_lain_all = models.transaksi_lain.objects.all()
    
    return render(request, 'transaksilain/transaksilain.html',{
        'transaksilainobj' : transaksi_lain_all
    })

@login_required
def create_transaksi_lain(request):
    if request.method == "GET":
        return render (request, "transaksilain/createtransaksilain.html")
    else:
        jenis_transaksi = request.POST["jenis_transaksi"]
        tanggal_transaksi = request.POST["tanggal_transaksi"]
        biaya = request.POST["biaya"]

        new_transaksi_lain = models.transaksi_lain(
            jenis_transaksi = jenis_transaksi,
            tanggal_transaksi = tanggal_transaksi,
            biaya = biaya
        )
        new_transaksi_lain.save()
        return redirect("transaksilain")
    
@login_required
def update_transaksi_lain(request, id):
    transaksi_lain_all = models.transaksi_lain.objects.get(id_transaksi = id)
    if request.method == "GET":
        tangal = datetime.strftime(transaksi_lain_all.tanggal_transaksi, '%Y-%m-%d')
        return render(request, "transaksilain/updatetransaksilain.html",{
            'transaksilainobj' : transaksi_lain_all, 
            'tanggal' : tangal
            })
    else :
        jenis_transaksi = request.POST["jenis_transaksi"]
        tanggal_transaksi = request.POST["tanggal_transaksi"]
        biaya = request.POST["biaya"]
        transaksi_lain_all.jenis_transaksi = jenis_transaksi
        transaksi_lain_all.tanggal_transaksi = tanggal_transaksi
        transaksi_lain_all.biaya = biaya
        transaksi_lain_all.save()
        return redirect('transaksilain')
    
@login_required
def delete_transaksi_lain(request,id):
    transaksi_lain_all = models.transaksi_lain.objects.get(id_transaksi=id)
    transaksi_lain_all.delete()
    return redirect('transaksilain')

@login_required
def panen(request):
    allpanenobj = models.panen.objects.all()
    return render(request, 'panen/panen.html', {
        "allpanenobj" : allpanenobj
        })

@login_required
def create_panen(request, id):
    try:
        mitraobj = models.mitra.objects.get(id_mitra=id)
    except models.mitra.DoesNotExist:
        return HttpResponse("Mitra not found")

    OrderFormSet = inlineformset_factory(
        models.panen,
        models.detail_panen,
        fields=('id_komoditas', 'jumlah', 'tanggalkadaluwarsa'),
        extra=2,
        can_delete=True,
        widgets={
            'tanggalkadaluwarsa': DateInput(attrs={'type': 'date'})
        }
    )

    if request.method == 'GET':
        formset = OrderFormSet(instance=models.panen(id_mitra=mitraobj))
        return render(request, 'detailpanen/createdetailpanen.html', {
            'mitraobj': mitraobj,
            'formset': formset
        })

    elif request.method == 'POST':
        formset = OrderFormSet(request.POST)
        if formset.is_valid():
            with transaction.atomic():
                panen_instance = models.panen.objects.create(id_mitra=mitraobj, tanggal_panen=datetime.now())
                formset.instance = panen_instance
                formset.save()
            return redirect('panen')

    context = {'formset': formset}
    return render(request, 'panen/createpanen.html', context)










# def create_panen(request, id):
#     if request.method == 'GET':
#         mitraobj = models.mitra.objects.get(id_mitra=id)
#         return render(request, 'panen/createpanen.html', {
#             'mitraobj': mitraobj
#         })

#     elif request.method == "POST":
#         tanggal_panen= datetime.now()

#         newpanen = models.panen.objects.create(
#             id_mitra_id=id,
#             tanggal_panen=tanggal_panen
#         )

#         return redirect('panen')

# def create_detailpanen(request, id):


#     OrderFormSet = inlineformset_factory(
#         models.panen,
#         models.detail_panen,
#         fields = ('id_komoditas', 'jumlah', 'tanggalkadaluwarsa'),
#         extra=2,
#         can_delete=True,
#     widgets={
#         'tanggalkadaluwarsa': DateInput(attrs={'type': 'date'})
#     }
#         )
#     panen = models.panen.objects.get(id_panen = id)
#     formset = OrderFormSet (instance = panen)
#     if request.method == 'POST':
#         formset = OrderFormSet (request.POST, instance = panen)
#         if formset.is_valid():  
#             formset.save()
#             return redirect('panen')
#     context = {'formset' : formset}
#     return render (request, 'detailpanen/createdetailpanen.html', context)


@login_required
def update_panen(request, id):
    panenobj = models.panen.objects.get(id_panen = id)
    if request.method == "GET":
        allmitraobj = models.mitra.objects.all()
        tanggal= datetime.strftime(panenobj.tanggal_panen, '%Y-%m-%d')
        return render(request, "panen/updatepanen.html",{
            'panenobj' : panenobj,
            'datamitra' : allmitraobj,
            'tanggal' : tanggal
            })
    else :
        id_mitra = request.POST['id_mitra']
        getidmitra = models.mitra.objects.get(id_mitra=id_mitra)
        panenobj.tanggal_panen = request.POST['tanggal_panen']
        panenobj.id_mitra = getidmitra
        panenobj.save()
        return redirect('panen')

@login_required
def delete_panen(request,id):
    panen_obj = models.panen.objects.get(id_panen = id)
    panen_obj.delete()
    return redirect('panen')


@login_required
def detailpanen(request):
    alldetailpanenobj = models.detail_panen.objects.all()
    print(alldetailpanenobj)
    return render(request, 'detailpanen/detailpanen.html', {
        "alldetailpanenobj" : alldetailpanenobj
        })