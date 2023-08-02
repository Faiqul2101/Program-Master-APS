from django.shortcuts import render, redirect
from . import models
from datetime import datetime
import calendar
from .decorators import role_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.forms import DateInput
from django.db import transaction
from django.core.exceptions import ValidationError
import json
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile

# Create your views here.


komoditas_to_produk_mapping = {
        'Pastry': ('Jambu Kristal', 0.33),
        'Keripik Cale': ('Cale', 0.25),
        'Teh Bunga Talang': ('Bunga Talang', 0.1),
        'Lemon Kering': ('Lemon', 0.2),
    }

#  LOGIN
@login_required(login_url="login")
def logoutview(request):
    logout(request)
    messages.info(request,"Berhasil Logout")
    return redirect('login')

def loginview(request):
    if request.user.is_authenticated:
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'karyawan':
            return redirect('mitra')
        elif group in ['admin', 'owner']:
            return redirect('home')
    else:
        return render(request,"login.html")

def performlogin(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        print(request)
        username_login = request.POST['username']
        password_login = request.POST['password']
        userobj = authenticate(request, username=username_login,password=password_login)
        print(userobj)
        if userobj is not None:
            login(request, userobj)
            messages.success(request,"Login success")
            if userobj.groups.filter(name='admin').exists() or userobj.groups.filter(name='owner').exists():
                return redirect("home")
            elif userobj.groups.filter(name='karyawan').exists():
                return redirect("mitra")
            
        else:
            messages.error(request,"Username atau Password salah !!!")
            return redirect("login")
        
@login_required(login_url="login")
def performlogout(request):
    logout(request)
    print("Anda keluar")
    return redirect("login")

# DASHBOARD 
@login_required(login_url="login")
@role_required(["owner", 'admin'])
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        
        # DATA BULANAN
        currentdate = datetime.now()
        tanggalmuda = datetime.now().date().replace(day=1)
        tanggaltua =  currentdate.replace(day=calendar.monthrange(currentdate.year,currentdate.month)[1])
        
        penjualanbulan = models.penjualan.objects.filter(tanggal_penjualan__range=(tanggalmuda,tanggaltua))
        pembelianbulan = models.panen.objects.filter(tanggal_panen__range=(tanggalmuda,tanggaltua))
        transaksibulan = models.transaksi_lain.objects.filter(tanggal_transaksi__range=(tanggalmuda,tanggaltua))

        penjualansebulan_produk = []
        penjualansebulan_komoditas = []
        pembeliansebulan = []
        transaksisebulan = []

        for item in penjualanbulan:
            getdetailjual = models.detail_penjualan.objects.filter(id_penjualan=item.id_penjualan)
            for i in getdetailjual:
                if i.id_komoditas is not None:
                    totalpenjualan_komoditas = i.id_komoditas.harga_jual*i.kuantitas_komoditas
                    penjualansebulan_komoditas.append(totalpenjualan_komoditas)
                if i.id_produk is not None:
                    totalpenjualan_produk = i.id_produk.hargaproduk*i.kuantitas_produk
                    penjualansebulan_produk.append(totalpenjualan_produk)
        print(f'Total Produk: {penjualansebulan_produk} \n Total Komoditas: {penjualansebulan_komoditas}')
        print(sum(penjualansebulan_produk))

        for item in pembelianbulan:
            getdetailbeli = models.detail_panen.objects.filter(id_panen=item.id_panen)
            for i in getdetailbeli:
                totalpembelian = i.id_komoditas.harga_beli*i.jumlah
                pembeliansebulan.append(totalpembelian)
        print('panen ', pembeliansebulan)
        
        for item in transaksibulan:
            totaltransaksi = item.biaya
            transaksisebulan.append(totaltransaksi)
        print(transaksisebulan)

        totalpenjualanbulanan = sum(penjualansebulan_komoditas) + sum(penjualansebulan_produk)
        totalpembelianbulanan = sum(pembeliansebulan)
        totaltransaksibulanan = sum(transaksisebulan)

        profitbulanan = totalpenjualanbulanan - totalpembelianbulanan - totaltransaksibulanan
        if profitbulanan > 0:
            format_profitbulanan = " {:,}".format(profitbulanan)
        else:
            format_profitbulanan = " Loss"
        format_penjualanbulanan = " {:,}".format(totalpenjualanbulanan)

        # DATA TAHUNAN
        tahunmulai = datetime.now().date().replace(month=1,day=1)
        tahunakhir = datetime.now().date().replace(month=12,day=31)

        penjualantahun = models.penjualan.objects.filter(tanggal_penjualan__range=(tahunmulai,tahunakhir))
        pembeliantahun = models.panen.objects.filter(tanggal_panen__range=(tahunmulai,tahunakhir))
        transaksitahun = models.transaksi_lain.objects.filter(tanggal_transaksi__range=(tahunmulai,tahunakhir))

        penjualansetahun_produk = []
        penjualansetahun_komoditas = []
        pembeliansetahun = []
        transaksisetahun = []

        for item in penjualantahun:
            getdetailjual = models.detail_penjualan.objects.filter(id_penjualan=item.id_penjualan)
            for i in getdetailjual:
                if i.id_komoditas is not None:
                    totalpenjualan_komoditas = i.id_komoditas.harga_jual*i.kuantitas_komoditas
                    penjualansetahun_komoditas.append(totalpenjualan_komoditas)
                if i.id_produk is not None:
                    totalpenjualan_produk = i.id_produk.hargaproduk*i.kuantitas_produk
                    penjualansetahun_produk.append(totalpenjualan_produk)

        for item in pembeliantahun:
            getdetailbeli = models.detail_panen.objects.filter(id_panen=item.id_panen)
            for i in getdetailbeli:
                totalpembelian = i.id_komoditas.harga_beli*i.jumlah
                pembeliansetahun.append(totalpembelian)

        for item in transaksitahun:
            totaltransaksi = item.biaya
            transaksisetahun.append(totaltransaksi)

        totalpenjualantahunan = sum(penjualansetahun_komoditas) + sum(penjualansetahun_produk)
        totalpembeliantahunan = sum(pembeliansetahun)
        totaltransaksitahunan = sum(transaksisetahun)

        profittahunan = totalpenjualantahunan - totalpembeliantahunan - totaltransaksitahunan
        if profittahunan > 0:
            format_profittahunan = " {:,}".format(profittahunan)
        else:
            format_profittahunan = " Loss"
        format_penjualantahunan = " {:,}".format(totalpenjualantahunan)


        # AREA CHART
        bulanke = int(currentdate.strftime("%m"))
        datajualperbulan = []

        for perbulan in range(1, bulanke + 1):
            tanggalmulai = datetime.now().date().replace(month=perbulan, day=1)
            tanggalakhir = currentdate.replace(
                month=perbulan, day=calendar.monthrange(currentdate.year, perbulan)[1]
            )
            penjualanperbulan = models.penjualan.objects.filter(
                tanggal_penjualan__range=(tanggalmulai, tanggalakhir)
            )
            jualperbulanan_komoditas = []
            jualperbulanan_produk = []
            for item in penjualanperbulan:
                getdetailjual = models.detail_penjualan.objects.filter(id_penjualan=item.id_penjualan)
                for i in getdetailjual:
                    if i.id_komoditas is not None:
                        totalpenjualan_komoditas = i.id_komoditas.harga_jual * i.kuantitas_komoditas
                        jualperbulanan_komoditas.append(totalpenjualan_komoditas)
                    if i.id_produk is not None:
                        totalpenjualan_produk = i.id_produk.hargaproduk * i.kuantitas_produk
                        jualperbulanan_produk.append(totalpenjualan_produk)
            totalperbulan_komoditas = sum(jualperbulanan_komoditas)
            totalperbulan_produk = sum(jualperbulanan_produk)
            datajualperbulan.append(totalperbulan_komoditas + totalperbulan_produk)
            
        print(datajualperbulan)

        # PIE CHART PASAR
        pasar_pendapatan = {}
        alldetailjual = models.detail_penjualan.objects.all()

        for item in alldetailjual:
            id_pasar = item.id_penjualan.id_pasar_id
            pendapatan = 0
            
            if item.id_produk:
                produk = models.produk.objects.get(id_produk=item.id_produk_id)
                pendapatan += produk.hargaproduk * item.kuantitas_produk

            if item.id_komoditas:
                komoditas = models.komoditas.objects.get(id_komoditas=item.id_komoditas_id)
                pendapatan += komoditas.harga_jual * item.kuantitas_komoditas
            
            if id_pasar in pasar_pendapatan:
                pasar_pendapatan[id_pasar] += pendapatan
            else:
                pasar_pendapatan[id_pasar] = pendapatan

        # Menghitung total pendapatan
        total_pendapatan = sum(pasar_pendapatan.values())

        # Membuat pie chart
        labels = []
        sizes = []

        for pasar_id, pendapatan in pasar_pendapatan.items():
            pasar = models.pasar.objects.get(id_pasar=pasar_id)
            labels.append(pasar.nama_pasar)
            sizes.append(pendapatan / total_pendapatan)
        print(labels)
        print(sizes)

        # PIE CHART KOMODITAS
        komoditas_pendapatan = {}
        produk_pendapatan = {}
        alldetailjual = models.detail_penjualan.objects.all()

        for item in alldetailjual:
            pendapatan = 0

            if item.id_produk:
                produk = models.produk.objects.get(id_produk=item.id_produk_id)
                pendapatan += produk.hargaproduk * item.kuantitas_produk
                if item.id_produk_id in produk_pendapatan:
                    produk_pendapatan[item.id_produk_id] += pendapatan
                else:
                    produk_pendapatan[item.id_produk_id] = pendapatan

            if item.id_komoditas:
                komoditas = models.komoditas.objects.get(id_komoditas=item.id_komoditas_id)
                pendapatan += komoditas.harga_jual * item.kuantitas_komoditas
                if item.id_komoditas_id in komoditas_pendapatan:
                    komoditas_pendapatan[item.id_komoditas_id] += pendapatan
                else:
                    komoditas_pendapatan[item.id_komoditas_id] = pendapatan

        total_pendapatan1 = sum(komoditas_pendapatan.values()) + sum(produk_pendapatan.values())
        # Menggabungkan data produk dan komoditas menjadi satu dictionary
        labels1 = []
        sizes1 = []

        # Menambahkan data produk ke labels dan sizes
        for produk_id, pendapatan in produk_pendapatan.items():
            produk = models.produk.objects.get(id_produk=produk_id)
            labels1.append(produk.namaproduk)
            sizes1.append(pendapatan/total_pendapatan1)

        # Menambahkan data komoditas ke labels dan sizes
        for komoditas_id, pendapatan in komoditas_pendapatan.items():
            komoditas = models.komoditas.objects.get(id_komoditas=komoditas_id)
            nama_komoditas = komoditas.nama_komoditas + " " + komoditas.id_grade.nama_grade
            labels1.append(nama_komoditas)
            sizes1.append(pendapatan/total_pendapatan1)

        print(labels1)
        print(sizes1)
        context = {
            "profitbulanan" : format_profitbulanan,
            "penjualanbulanan" : format_penjualanbulanan,
            "penjualantahunan" : format_penjualantahunan,
            "profittahunan" : format_profittahunan,
            "datajualperbulan_json" : json.dumps(datajualperbulan),
            'labels' : json.dumps(labels),
            'sizes' : json.dumps(sizes),
            'labels1' : json.dumps(labels1),
            'sizes1' : json.dumps(sizes1)
        }
        return render(request, 'index.html', context)

# MITRA

@login_required
@role_required(["owner", 'admin', 'karyawan'])
def mitra(request):
    mitraobj = models.mitra.objects.all()
    
    return render(request, 'mitra/mitra.html', {
        'mitraobj' : mitraobj,
    })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
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

@login_required(login_url="login")
@role_required(["owner", 'admin'])
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

@login_required(login_url="login")
@role_required(["owner", 'admin'])
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

@login_required(login_url="login")
@role_required(["owner"])
def delete_mitra(request,id):
    mitraobj = models.mitra.objects.get(id_mitra = id)
    mitraobj.delete()
    return redirect('mitra')

# GRADE
@login_required(login_url="login")
@role_required(["owner"])
def grade(request):
    gradeobj = models.grade.objects.all()
    return render(request, 'grade/grade.html', {
        'gradeobj' : gradeobj
    })

@login_required(login_url="login")
@role_required(["owner"])
def create_grade(request):
    if request.method == "GET":
        return render(request, "grade/creategrade.html")
    else:
        nama_grade = request.POST["nama_grade"]
        deskripsi = request.POST["deskripsi"]

        models.grade(
            nama_grade = nama_grade,
            deskripsi = deskripsi
        ).save()
        return redirect('grade')

@login_required(login_url="login")
@role_required(["owner"])
def update_grade(request, id):
    gradeobj = models.grade.objects.get(id_grade = id)
    if request.method == "GET":
        return render(request, "grade/updategrade.html", {
            "gradeobj" : gradeobj
        })
    else:
        gradeobj.nama_grade = request.POST["nama_grade"]
        gradeobj.deskripsi = request.POST["deskripsi"]
        gradeobj.save()
        return redirect('grade')

@login_required(login_url="login")
@role_required(["owner"])
def delete_grade(request, id):
    gradeobj = models.grade.objects.get(id_grade = id)
    gradeobj.delete()
    return redirect('grade')

# PRODUK

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def produk(request):
    allprodukobj = models.produk.objects.all()

    return render (request, 'produk/produk.html',{
        'allprodukobj' : allprodukobj,
        })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def create_produk(request):
    if request.method == "GET" :
        return render(request, 'produk/createproduk.html', )
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


@login_required(login_url="login")
@role_required(["owner", 'admin'])
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

@login_required(login_url="login")
@role_required(["owner"])
def delete_produk(request, id):
    produkobj = models.produk.objects.get(id_produk=id)
    produkobj.delete()
    return redirect('produk')

# PASAR

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def pasar(request):
    pasarobj = models.pasar.objects.all()
    # is_admin = request.user.groups.filter(name='Admin').exists()
    # is_pegawai = request.user.groups.filter(name='Pegawai').exists()

    return render(request, 'pasar/pasar.html', {
        'pasarobj' : pasarobj,
    })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
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

@login_required(login_url="login")
@role_required(["owner", 'admin'])
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

@login_required(login_url="login")
@role_required(["owner"])
def delete_pasar(request,id):
    pasarobj = models.pasar.objects.get(id_pasar = id)
    pasarobj.delete()
    return redirect('pasar')

@login_required(login_url="login")
@role_required(["owner", 'admin', 'karyawan'])
def komoditas(request):
    allkomoditasobj = models.komoditas.objects.all()
    stok = stok_keseluruhan()
    keseluruhan = []
    for item in allkomoditasobj:
        for x in stok:
            if item.nama_komoditas + ' ' + item.id_grade.nama_grade == x['komoditas']:
                keseluruhan.append((item , x['stok']))
    print(keseluruhan)
    
    return render(request, 'komoditas/komoditas.html', {
        'tuple': keseluruhan,
    })

@login_required(login_url="login")
@role_required(["owner", 'karyawan'])
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

        new_komoditas = models.komoditas.objects.create(
            id_grade_id = id_grade,
            nama_komoditas = nama_komoditas,
            harga_beli=harga_beli, 
            harga_jual=harga_jual
            )

        return redirect('komoditas')

@login_required(login_url="login")
@role_required(["owner", 'karyawan'])
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
    
@login_required(login_url="login")
@role_required(["owner"])
def delete_komoditas(request, id):
    komoditasobj = models.komoditas.objects.get(id_komoditas=id)
    komoditasobj.delete()
    return redirect('komoditas')

# TRANSAKSI LAIN

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def transaksi_lain(request):
    transaksi_lain_all = models.transaksi_lain.objects.all()
    
    return render(request, 'transaksilain/transaksilain.html',{
        'transaksilainobj' : transaksi_lain_all
    })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
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
    
@login_required(login_url="login")
@role_required(["owner", 'admin'])
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
    
@login_required(login_url="login")
@role_required(["owner"])
def delete_transaksi_lain(request,id):
    transaksi_lain_all = models.transaksi_lain.objects.get(id_transaksi=id)
    transaksi_lain_all.delete()
    return redirect('transaksilain')

# PANEN

@login_required(login_url="login")
@role_required(["owner", 'admin', 'karyawan'])
def panen(request):
    allpanenobj = models.panen.objects.all()
    return render(request, 'panen/panen.html', {
        "allpanenobj" : allpanenobj
        })


@login_required(login_url="login")
@role_required(["owner", 'karyawan'])
def create_panen(request, id):
    try:
        mitraobj = models.mitra.objects.get(id_mitra=id)
    except models.mitra.DoesNotExist:
        return HttpResponse("Mitra not found")

    OrderFormSet = inlineformset_factory(
        models.panen,
        models.detail_panen,
        fields=('id_komoditas', 'jumlah', 'tanggalkadaluwarsa'),
        extra=10,
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
                komoditas_to_produk_mapping = {
                    'Jambu Kristal': ('Pastry', 3),
                    'Cale': ('Keripik Cale', 4),
                }

                for form in formset:
                    id_komoditas = form.cleaned_data.get('id_komoditas')
                    if id_komoditas:
                        komoditas_obj = models.komoditas.objects.get(id_komoditas=id_komoditas.id_komoditas)
                        if komoditas_obj.id_grade.nama_grade == 'Olah' and komoditas_obj.nama_komoditas in komoditas_to_produk_mapping:
                            produk_name, multiplier = komoditas_to_produk_mapping[komoditas_obj.nama_komoditas]
                            try:
                                existing_produk = models.produk.objects.get(namaproduk=produk_name)
                                stok_tersedia = komoditas_obj.get_stok_tersedia()
                                existing_produk.stok_produk = stok_tersedia * multiplier
                                existing_produk.save()
                            except models.produk.DoesNotExist:
                                pass
                formset.save()
                # Update stok_produk for "Olah" komoditas
            return redirect('detailpanen')

    context = {'formset': formset}
    return render(request, 'detailpanen/createdetailpanen.html', context)

@login_required(login_url="login")
@role_required(["owner", 'karyawan'])
def ubah_panen(request, id):
    OrderFormSet = inlineformset_factory(models.panen, 
                                        models.detail_panen,
                                        fields=('id_komoditas', 'jumlah', 'tanggalkadaluwarsa'),
                                        widgets={
                                                'tanggalkadaluwarsa': DateInput(attrs={'type': 'date'})
                                                },
                                        extra=1
                                        )

    panen= models.panen.objects.get(id_panen = id)
    formset = OrderFormSet (instance = panen)
    if request.method == 'POST':
        formset = OrderFormSet (request.POST, instance = panen)
        if formset.is_valid():  
            formset.save()
            return redirect('ubahdetailpanen', id=panen.id_panen, )
        
    context = {'formset' : formset}
    return render (request, 'detailpanen/ubahdetailpanen.html', context)

@role_required(["owner", 'karyawan'])
@login_required(login_url="login")
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

@login_required(login_url="login")
@role_required(["owner"])
def delete_panen(request,id):
    panen_obj = models.panen.objects.get(id_panen = id)
    panen_obj.delete()
    return redirect('panen')

# DETAIL PANEN

@login_required(login_url="login")
@role_required(["owner", 'admin', 'karyawan'])
def detailpanen(request):
    alldetailpanenobj = models.detail_panen.objects.all()
    detailpanen_olah = models.detail_panen.objects.filter(id_komoditas__id_grade__nama_grade = "Olah")
    print(alldetailpanenobj)
    return render(request, 'detailpanen/detailpanen.html', {
        "alldetailpanenobj" : alldetailpanenobj,
        'detailpanen_olah' : detailpanen_olah
        })

@login_required(login_url="login")
@role_required(["owner", 'karyawan'])
def update_detailpanen(request, id):
    detailpanenobj = models.detail_panen.objects.get(id_detailpanen=id)
    allkomoditasobj = models.komoditas.objects.all()

    if request.method == "GET":
        tanggal = detailpanenobj.tanggalkadaluwarsa.strftime('%Y-%m-%d')
        return render(request, 'detailpanen/updatedetailpanen.html', {
            'alldetailpanen': detailpanenobj,
            'datakomoditas': allkomoditasobj,
            'tanggal': tanggal
        })
    elif request.method == "POST":
        id_komoditas = request.POST["id_komoditas"]
        getidkomoditas = models.komoditas.objects.get(id_komoditas=id_komoditas)
        jumlah = request.POST["jumlah"]
        tanggal_kadaluwarsa = request.POST["tanggalkadaluwarsa"]

        detailpanenobj.id_komoditas = getidkomoditas
        detailpanenobj.jumlah = jumlah
        detailpanenobj.tanggalkadaluwarsa = tanggal_kadaluwarsa
        detailpanenobj.save()

        return redirect('detailpanen')
    
@login_required(login_url="login")
@role_required(["owner"])
def delete_detailpanen(request,id):
    detailpanenobj = models.detail_panen.objects.get(id_detailpanen=id)
    detailpanenobj.delete()
    return redirect('detailpanen')

# PENJUALAN 

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def penjualan(request):
    penjualanobj = models.penjualan.objects.all()
    return render (request, 'penjualan/penjualan.html',{
        'penjualanobj' : penjualanobj
    })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def updatepenjualan(request,id):
    penjualanobj = models.penjualan.objects.get(id_penjualan=id)
    datapasar = models.pasar.objects.all()
    if request.method == "GET":
        tanggal = datetime.strftime(penjualanobj.tanggal_penjualan, '%Y-%m-%d')
        return render(request, 'penjualan/updatepenjualan.html', {
            'penjualanobj' : penjualanobj,
            'tanggal' : tanggal,
            "datapasar" : datapasar
        })
    else:
        penjualanobj.tanggal_penjualan = request.POST['tanggalpenjualan']
        id_pasar = request.POST['id_pasar']
        getidpasar = models.pasar.objects.get(id_pasar=id_pasar)
        penjualanobj.id_pasar = getidpasar
        penjualanobj.save()
        return redirect('penjualan')

@login_required(login_url="login")
@role_required(["owner"])
def deletepenjualan(request, id):
    penjualanobj = models.penjualan.objects.get(id_penjualan = id)
    penjualanobj.delete()
    return redirect ('penjualan')


# DETAIL PENJUALAN

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def detail_penjualan(request):
    detailpenjualanobj = models.detail_penjualan.objects.all()
    return render(request, 'detailpenjualan/detailpenjualan.html', {
        'detailpenjualanobj': detailpenjualanobj
    })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def detail_penjualan_komoditas(request):
    detailpenjualanobj = models.detail_penjualan.objects.exclude(id_komoditas=None)
    return render(request, 'detailpenjualan/detailpenjualan_komoditas.html', {
        'detailpenjualanobj': detailpenjualanobj
    })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def detail_penjualan_produk(request):
    detailpenjualanobj = models.detail_penjualan.objects.exclude(id_produk=None)
    return render(request, 'detailpenjualan/detailpenjualan_produk.html', {
        'detailpenjualanobj': detailpenjualanobj
    })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def cerate_penjualan(request):
    if request.method == 'GET':
        pasarobj = models.pasar.objects.all()
        return render(request, 'penjualan/createpenjualan.html', {
            'datapasar' : pasarobj
        })
    elif request.method == 'POST':
        id_pasar = request.POST["id_pasar"]
        tanggal_penjualan = request.POST["tanggal_penjualan"]

        newpenjualan = models.penjualan.objects.create(
            id_pasar_id = id_pasar,
            tanggal_penjualan = tanggal_penjualan
        )
        newid = newpenjualan.id_penjualan

        return redirect('penjualan')

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def create_detailpenjualan_produk(request, id):
    OrderFormSet = inlineformset_factory(
        models.penjualan,
        models.detail_penjualan,
        fields=('id_produk', 'kuantitas_produk'),
        extra=1
    )
    
    penjualan_obj = models.penjualan.objects.get(id_penjualan=id)
    
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=penjualan_obj)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for form in formset:
                        id_produk = form.cleaned_data.get('id_produk')
                        kuantitas_komoditas = form.cleaned_data.get('kuantitas_produk')
                        if id_produk and kuantitas_komoditas:
                            produk_obj = models.produk.objects.get(id_produk=id_produk.id_produk)

                            if produk_obj.namaproduk in komoditas_to_produk_mapping:
                                komoditas_grade_olah, factor = komoditas_to_produk_mapping[produk_obj.namaproduk]

                                # Calculate the quantity of commodity produced based on the sales of the product
                                produced_commodity_quantity = kuantitas_komoditas * factor

                                # Check if the stock of the related processed commodity is sufficient
                                stok_tersedia = stok_olah()
                                for stok_item in stok_tersedia:
                                    if stok_item['komoditas'] == komoditas_grade_olah + ' Olah':
                                        if stok_item['stok'] >= produced_commodity_quantity:
                                            detail_penjualan_obj = form.save(commit=False)
                                            detail_penjualan_obj.id_penjualan = penjualan_obj
                                            detail_penjualan_obj.save()

                                            # Update the stock quantity of the related processed commodity
                                            stok_item['stok'] -= produced_commodity_quantity
                                        else:
                                            form.add_error('kuantitas_produk', 'Jumlah Produk melebihi stok yang tersedia.')
                                            raise ValidationError('Jumlah Produk melebihi stok yang tersedia.')
                                        break
                                else:
                                    # The related processed commodity was not found in the stok_tersedia list
                                    form.add_error('id_produk', 'Produk tidak ada dalam daftar pemetaan komoditas.')
                                    raise ValidationError('Produk tidak ada dalam daftar pemetaan komoditas.')

                return redirect('detailpenjualan_produk')
            except ValidationError as e:
                # Tangkap ValidationError dan tambahkan kesalahan ke form individu dalam formset
                for form in formset:
                    if form.has_error('kuantitas_produk') or form.has_error('id_produk'):
                        form.add_error(None, e)

    else:
        formset = OrderFormSet(instance=penjualan_obj)

    return render(request, 'detailpenjualan/createdetailpenjualan_produk.html', {'formset': formset, 'penjualan': penjualan_obj})

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def create_detailpenjualan_komoditas(request, id):
    OrderFormSet = inlineformset_factory(
        models.penjualan,
        models.detail_penjualan,
        fields=('id_komoditas', 'kuantitas_komoditas'),
        extra=1
    )
    
    penjualan_obj = models.penjualan.objects.get(id_penjualan=id)
    
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=penjualan_obj)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for form in formset:
                        id_komoditas = form.cleaned_data.get('id_komoditas')
                        kuantitas_komoditas = form.cleaned_data.get('kuantitas_komoditas')
                        if id_komoditas and kuantitas_komoditas:
                            komoditas_obj = models.komoditas.objects.get(id_komoditas=id_komoditas.id_komoditas)
                            stok_tersedia = stok_awal([komoditas_obj])
                            stok_tersedia_komoditas = stok_tersedia[0]['stok']
                            if kuantitas_komoditas > stok_tersedia_komoditas:
                                form.add_error('kuantitas_komoditas', 'Jumlah komoditas melebihi stok yang tersedia.')
                                raise ValidationError('Jumlah komoditas melebihi stok yang tersedia.')
                            else:
                                detail_penjualan_obj = form.save(commit=False)
                                detail_penjualan_obj.id_penjualan = penjualan_obj
                                detail_penjualan_obj.save()

                return redirect('detailpenjualan_komoditas')
            except ValidationError as e:
                # Tangkap ValidationError dan tambahkan kesalahan ke form individu dalam formset
                for form in formset:
                    if form.has_error('kuantitas_komoditas'):
                        form.add_error('kuantitas_komoditas', e)
    else:
        formset = OrderFormSet(instance=penjualan_obj)
    
    return render(request, 'detailpenjualan/createdetailpenjualan_komoditas.html', {'formset': formset, 'penjualan': penjualan_obj})

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def update_detailpenjualan(request, id):
    getdetailpenjualan = models.detail_penjualan.objects.get(id_detailpenjualan = id)
    if request.method == "GET":
        komoditasobj = models.komoditas.objects.all()
        produkobj = models.produk.objects.all()
        return render (request, 'detailpenjualan/updatedetailpenjualan.html', {
            'detailjualobj' : getdetailpenjualan,
            'datakomoditas' : komoditasobj,
            'dataproduk' : produkobj
        })
    else:
        id_komoditas = request.POST['id_komoditas']
        getidkomoditas = models.komoditas.objects.get(id_komoditas = id_komoditas)
        kuantitas_komoditas = request.POST['kuantitas_komoditas']
        id_produk = request.POST['id_produk']
        getidproduk = models.produk.objects.get(id_produk = id_produk)
        kuantitas_produk = request.POST['kuantitas_produk']

        getdetailpenjualan.id_komoditas = getidkomoditas
        getdetailpenjualan.id_produk = getidproduk

        if kuantitas_komoditas == "":
            getdetailpenjualan.id_komoditas = None
            kuantitas_komoditas = None
        elif kuantitas_produk == "":
            getdetailpenjualan.id_produk = None
            kuantitas_produk = None

        getdetailpenjualan.kuantitas_produk = kuantitas_produk
        getdetailpenjualan.kuantitas_komoditas = kuantitas_komoditas
        getdetailpenjualan.save()
        return redirect("detailpenjualan")

@login_required(login_url="login")
@role_required(["owner"])
def delete_detailpenjualan(request,id):
    getdetailpenjualan = models.detail_penjualan.objects.get(id_detailpenjualan = id)
    getdetailpenjualan.delete()
    return redirect('detailpenjualan')

def stok_awal(obj):
    stok_per_komoditas =[]
    for i in obj:
        dummy = {}
        totalpenjualan =0
        totalpanen =0
        a = models.detail_penjualan.objects.filter(id_komoditas = i.id_komoditas)
        # print('aaa',a,'aaa')
        for x in a:
            totalpenjualan += x.kuantitas_komoditas
        b = models.detail_panen.objects.filter(id_komoditas=i.id_komoditas)
        for x in b:
            totalpanen += x.jumlah
        totalstok = totalpanen - totalpenjualan
        dummy['komoditas'] = i.nama_komoditas + ' ' + i.id_grade.nama_grade
        dummy['stok'] = totalstok
        stok_per_komoditas.append(dummy)

        

    return stok_per_komoditas
        

def stok_olah():
    produkobj = models.produk.objects.all()
    obj = models.komoditas.objects.filter(id_grade__nama_grade="Olah")
    stok_olah = stok_awal(obj)

    for i in produkobj:
        getdetailjual = models.detail_penjualan.objects.filter(id_produk=i.id_produk)
        kuantitasproduk = 0
        for x in getdetailjual:
            kuantitasproduk += x.kuantitas_produk

        print(f"Total quantity of {i.namaproduk} sold: {kuantitasproduk}")

        if i.namaproduk in komoditas_to_produk_mapping:
            komoditas_grade_olah, factor = komoditas_to_produk_mapping[i.namaproduk]
            komoditas_dibutuhkan = kuantitasproduk * factor
            for z in stok_olah:
                if z['komoditas'] == komoditas_grade_olah + ' Olah':
                    z['stok'] -= komoditas_dibutuhkan

    return stok_olah

def stok_keseluruhan():
    obj1 = models.komoditas.objects.exclude(id_grade__nama_grade = "Olah")
    
    list1 = stok_awal(obj1)
    list2 = stok_olah()

    gabungan = list1 + list2

    return gabungan

@login_required(login_url="login")
@role_required(["owner"])
def laporan_laba_rugi(request):
    if request.method == "GET":
        return render(request,'laporanlabarugi/laporan.html')
    elif request.method == "POST":
        mulai = request.POST['mulai']
        akhir = request.POST['akhir']

        # PENJUALAN
        penjualanrange = models.penjualan.objects.filter(tanggal_penjualan__range = (mulai, akhir))

        penjualansebulan_produk = []
        penjualansebulan_komoditas = []
        pembeliansebulan = []
        transaksisebulan = []

        for item in penjualanrange:
            getdetailjual = models.detail_penjualan.objects.filter(id_penjualan=item.id_penjualan)
            
            for i in getdetailjual:
                if i.id_komoditas is not None:
                    totalpenjualan_komoditas = i.id_komoditas.harga_jual*i.kuantitas_komoditas
                    penjualansebulan_komoditas.append(totalpenjualan_komoditas)
                if i.id_produk is not None:
                    totalpenjualan_produk = i.id_produk.hargaproduk*i.kuantitas_produk
                    penjualansebulan_produk.append(totalpenjualan_produk)

        totalpenjualan = sum(penjualansebulan_komoditas) + sum(penjualansebulan_produk)

        # HPP dan BIAYA LAIN
        pembelianrange = models.panen.objects.filter(tanggal_panen__range=(mulai,akhir))

        for item in pembelianrange:
            getdetailbeli = models.detail_panen.objects.filter(id_panen=item.id_panen)
            for i in getdetailbeli:
                totalpembelian = i.id_komoditas.harga_beli*i.jumlah
                pembeliansebulan.append(totalpembelian)

        totalpanen = sum(pembeliansebulan)

        transaksirange = models.transaksi_lain.objects.filter(tanggal_transaksi__range=(mulai,akhir))
        biayahpp = ["Biaya Tenaga Kerja" , "Biaya Listrik" , "Biaya Air"]
        biayapemasaran = 0
        biayaadministrasi = 0
        biayapajak = 0

        for item in transaksirange:
            if item.jenis_transaksi in biayahpp:
                transaksisebulan.append(item.biaya)
            elif item.jenis_transaksi == "Biaya Pemasaran":
                biayapemasaran += item.biaya
            elif item.jenis_transaksi == "Biaya Administrasi":
                biayaadministrasi += item.biaya
            elif item.jenis_transaksi == "Biaya Pajak":
                biayapajak += item.biaya

        totaltransaksi = sum(transaksisebulan)
        totalbebanusaha = biayapemasaran + biayaadministrasi
        totalhpp = totalpanen + totaltransaksi
        
        # LABA / RUGI
        labarugi = totalpenjualan - totalhpp  

        # LABA SEBELUM PAJAK
        labasebelumpajak = labarugi -totalbebanusaha
        
        # LABA BERSIH
        lababersih = labasebelumpajak - biayapajak

        return render(request, 'laporanlabarugi/laporanlabarugi.html', {
            "penjualan" : totalpenjualan,
            "hpp" : totalhpp,
            "labarugi" : labarugi,
            "pemasaran" : biayapemasaran,
            "administrasi" : biayaadministrasi,
            "totalbebanusaha": totalbebanusaha,
            "labasebelumpajak" : labasebelumpajak,
            "pajak" : biayapajak,
            "lababersih" : lababersih,
            'tanggalmulai': mulai,
            'tanggalakhir': akhir,
        })
    
@login_required(login_url="login")
@role_required(["owner"])
def laporan_laba_rugi_pdf(request,mulai,akhir):
    # PENJUALAN
    penjualanrange = models.penjualan.objects.filter(tanggal_penjualan__range = (mulai, akhir))

    penjualansebulan_produk = []
    penjualansebulan_komoditas = []
    pembeliansebulan = []
    transaksisebulan = []

    for item in penjualanrange:
        getdetailjual = models.detail_penjualan.objects.filter(id_penjualan=item.id_penjualan)
        
        for i in getdetailjual:
            if i.id_komoditas is not None:
                totalpenjualan_komoditas = i.id_komoditas.harga_jual*i.kuantitas_komoditas
                penjualansebulan_komoditas.append(totalpenjualan_komoditas)
            if i.id_produk is not None:
                totalpenjualan_produk = i.id_produk.hargaproduk*i.kuantitas_produk
                penjualansebulan_produk.append(totalpenjualan_produk)

    totalpenjualan = sum(penjualansebulan_komoditas) + sum(penjualansebulan_produk)

    # HPP dan BIAYA LAIN
    pembelianrange = models.panen.objects.filter(tanggal_panen__range=(mulai,akhir))

    for item in pembelianrange:
        getdetailbeli = models.detail_panen.objects.filter(id_panen=item.id_panen)
        for i in getdetailbeli:
            totalpembelian = i.id_komoditas.harga_beli*i.jumlah
            pembeliansebulan.append(totalpembelian)

    totalpanen = sum(pembeliansebulan)

    transaksirange = models.transaksi_lain.objects.filter(tanggal_transaksi__range=(mulai,akhir))
    biayahpp = ["Biaya Tenaga Kerja" , "Biaya Listrik" , "Biaya Air"]
    biayapemasaran = 0
    biayaadministrasi = 0
    biayapajak = 0

    for item in transaksirange:
        if item.jenis_transaksi in biayahpp:
            transaksisebulan.append(item.biaya)
        elif item.jenis_transaksi == "Biaya Pemasaran":
            biayapemasaran += item.biaya
        elif item.jenis_transaksi == "Biaya Administrasi":
            biayaadministrasi += item.biaya
        elif item.jenis_transaksi == "Biaya Pajak":
            biayapajak += item.biaya

    totaltransaksi = sum(transaksisebulan)
    totalbebanusaha = biayapemasaran + biayaadministrasi
    totalhpp = totalpanen + totaltransaksi
    
    # LABA / RUGI
    labarugi = totalpenjualan - totalhpp  

    # LABA SEBELUM PAJAK
    labasebelumpajak = labarugi -totalbebanusaha
    
    # LABA BERSIH
    lababersih = labasebelumpajak - biayapajak

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_of_students.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string(
        'laporanlabarugi/laporanlabarugipdf.html',{
            "penjualan" : totalpenjualan,
            "hpp" : totalhpp,
            "labarugi" : labarugi,
            "pemasaran" : biayapemasaran,
            "administrasi" : biayaadministrasi,
            "totalbebanusaha": totalbebanusaha,
            "labasebelumpajak" : labasebelumpajak,
            "pajak" : biayapajak,
            "lababersih" : lababersih,
            'tanggalmulai': mulai,
            'tanggalakhir': akhir,
            })
    
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    render(request, 'laporanlabarugi/laporanlabarugipdf.html')
    
    return response

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def laporanpenjualan(request):
    if request.method == "GET":
        return render(request, 'laporanpenjualan/laporanjual.html')
    elif request.method == "POST":
        detailobj = []

        mulai = request.POST['mulai']
        akhir = request.POST['akhir']

        getlaporanpenjualan = models.penjualan.objects.filter(tanggal_penjualan__range=(mulai, akhir))
        listtotalbanget = []
        for item in getlaporanpenjualan:
            datadetailobj = []
            getdetailobject = models.detail_penjualan.objects.filter(id_penjualan_id = item.id_penjualan)
            datadetailobj.append(item)
            datadetailobj.append(getdetailobject)
            listtotal = []
            for i in getdetailobject:
                if i.id_komoditas is not None:
                    totalpenjualankom = i.id_komoditas.harga_jual*i.kuantitas_komoditas
                    listtotal.append(totalpenjualankom)
                if i.id_produk is not None:
                    totalpenjualanprod = i.id_produk.hargaproduk*i.kuantitas_produk
                    listtotal.append(totalpenjualanprod)
            datadetailobj.append(listtotal)
            totalbanget = sum(listtotal)
            listtotalbanget.append(totalbanget)
            datadetailobj.append(totalbanget)
            detailobj.append(datadetailobj)
        totalkeseluruhan = sum(listtotalbanget)

        print(detailobj)

        return render(request, 'laporanpenjualan/laporanpenjualan.html', {
            'detailobjek' : detailobj,
            'tanggalmulai': mulai,
            'tanggalakhir': akhir,
            'pemasukan': totalkeseluruhan
        })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def laporanpenjualanpdf (request, mulai, akhir):
    detailobj = []

    getlaporanpenjualan = models.penjualan.objects.filter(tanggal_penjualan__range=(mulai, akhir))
    listtotalbanget = []
    for item in getlaporanpenjualan:
        datadetailobj = []
        getdetailobject = models.detail_penjualan.objects.filter(id_penjualan_id = item.id_penjualan)
        datadetailobj.append(item)
        datadetailobj.append(getdetailobject)
        listtotal = []
        for i in getdetailobject:
            if i.id_komoditas is not None:
                totalpenjualankom = i.id_komoditas.harga_jual*i.kuantitas_komoditas
                listtotal.append(totalpenjualankom)
            if i.id_produk is not None:
                totalpenjualanprod = i.id_produk.hargaproduk*i.kuantitas_produk
                listtotal.append(totalpenjualanprod)
        datadetailobj.append(listtotal)
        totalbanget = sum(listtotal)
        listtotalbanget.append(totalbanget)
        datadetailobj.append(totalbanget)
        detailobj.append(datadetailobj)
    totalkeseluruhan = sum(listtotalbanget)

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_of_students.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string(
        'laporanpenjualan/laporanpenjualanpdf.html',{
            'detailobj' : detailobj,
            'pemasukan' : totalkeseluruhan,
            'tanggalmulai': mulai,
            'tanggalakhir': akhir,
            })
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    render(request, 'laporanpenjualan/laporanpenjualanpdf.html')
    
    return response

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def laporanpanen(request):
    if request.method == "GET":
        return render(request, 'laporanpanen/laporan.html')
    elif request.method == "POST":
        detailobj = []

        mulai = request.POST['mulai']
        akhir = request.POST['akhir']

        getlaporanpanen = models.panen.objects.filter(tanggal_panen__range=(mulai, akhir))
        listtotalbanget = []
        for item in getlaporanpanen:
            datadetailobj = []
            getdetailobject = models.detail_panen.objects.filter(id_panen_id = item.id_panen)
            datadetailobj.append(item)
            datadetailobj.append(getdetailobject)
            listtotal = []
            for i in getdetailobject:
                totalpembelian = i.id_komoditas.harga_beli*i.jumlah
                listtotal.append(totalpembelian)
            datadetailobj.append(listtotal)
            totalbanget = sum(listtotal)
            listtotalbanget.append(totalbanget)
            datadetailobj.append(totalbanget)
            detailobj.append(datadetailobj)
        totalkeseluruhan = sum(listtotalbanget)

        print(detailobj)

        return render(request, 'laporanpanen/laporanpanen.html', {
            'detailobjek' : detailobj,
            'tanggalmulai': mulai,
            'tanggalakhir': akhir,
            'pengeluaran': totalkeseluruhan
        })

@login_required(login_url="login")
@role_required(["owner", 'admin'])
def laporanpanenpdf (request, mulai, akhir):
    detailobj = []

    getlaporanpanen = models.panen.objects.filter(tanggal_panen__range=(mulai, akhir))
    listtotalbanget = []
    for item in getlaporanpanen:
        datadetailobj = []
        getdetailobject = models.detail_panen.objects.filter(id_panen_id = item.id_panen)
        datadetailobj.append(item)
        datadetailobj.append(getdetailobject)
        listtotal = []
        for i in getdetailobject:
            totalpembelian = i.id_komoditas.harga_beli*i.jumlah
            listtotal.append(totalpembelian)
        datadetailobj.append(listtotal)
        totalbanget = sum(listtotal)
        listtotalbanget.append(totalbanget)
        datadetailobj.append(totalbanget)
        detailobj.append(datadetailobj)
    totalkeseluruhan = sum(listtotalbanget)

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_of_students.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string(
        'laporanpanen/laporanpanenpdf.html',{
            'detailobj' : detailobj,
            'pemasukan' : totalkeseluruhan,
            'tanggalmulai': mulai,
            'tanggalakhir': akhir,
            })
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    render(request, 'laporanpanen/laporanpanenpdf.html')
    
    return response