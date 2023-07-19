from django.shortcuts import render, redirect
from . import models
from datetime import datetime
import calendar
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.forms import DateInput
from django.db import transaction
import matplotlib.pyplot as plt
import json
# Create your views here.

#  LOGIN
@login_required
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'loginsiam.html')
    else:
        getdatabeli = models.detail_panen.objects.all()
        getdatajual = models.detail_penjualan.objects.all()
        
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
            print('get', getdetailjual)
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

        # PIE CHART
        pasar_pendapatan = {}
        alldetailjual = models.detail_penjualan.objects.all()

        for item in alldetailjual:
            id_pasar = item.id_penjualan.id_pasar_id
            pendapatan = 0
            
            if item.id_produk:
                produk = models.produk.objects.get(id_produk=item.id_produk_id)
                pendapatan += produk.hargaproduk * item.kuantitas_produk
            elif item.id_komoditas:
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
        context = {
            "profitbulanan" : format_profitbulanan,
            "penjualanbulanan" : format_penjualanbulanan,
            "penjualantahunan" : format_penjualantahunan,
            "profittahunan" : format_profittahunan,
            "datajualperbulan_json" : json.dumps(datajualperbulan),
            'labels' : json.dumps(labels),
            'sizes' : json.dumps(sizes)
        }
        return render(request, 'index.html', context)




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


# MITRA

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

# GRADE

def grade(request):
    gradeobj = models.grade.objects.all()
    return render(request, 'grade/grade.html', {
        'gradeobj' : gradeobj
    })

# PRODUK

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

# PASAR

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

# KOMODITAS

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

# TRANSAKSI LAIN

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

# PANEN

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
                formset.save()
            return redirect('detailpanen')

    context = {'formset': formset}
    return render(request, 'detailpanen/createdetailpanen.html', context)

@login_required
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

# PENJUALAN 

@login_required
def penjualan(request):
    penjualanobj = models.penjualan.objects.all()
    return render (request, 'penjualan/penjualan.html',{
        'penjualanobj' : penjualanobj
    })

def detail_penjualan_komoditas(request):
    detailpenjualanobj = models.detail_penjualan.objects.exclude(id_komoditas=None)
    return render(request, 'detailpenjualan/detailpenjualan_komoditas.html', {
        'detailpenjualanobj': detailpenjualanobj
    })

def detail_penjualan_produk(request):
    detailpenjualanobj = models.detail_penjualan.objects.exclude(id_produk=None)
    return render(request, 'detailpenjualan/detailpenjualan_produk.html', {
        'detailpenjualanobj': detailpenjualanobj
    })
def jual(request):
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
        # return redirect('penjualan')
        return redirect('penjualan')

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
            # for form in formset:
            #     kuantitas_komoditas = form.cleaned_data.get('kuantitas_komoditas')
            #     if kuantitas_komoditas is None:
            #         form.instance.kuantitas_komoditas = 0
            formset.save()
            return redirect('detailpenjualan_produk')
    else:
        formset = OrderFormSet(instance=penjualan_obj)

    return render(request, 'detailpenjualan/createdetailpenjualan_produk.html', {'formset': formset, 'penjualan': penjualan_obj})
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
            # for form in formset:
            #     kuantitas_produk = form.cleaned_data.get('kuantitas_produk')
            #     if kuantitas_produk is None:
            #         form.instance.kuantitas_produk = 0
            formset.save()
            return redirect('detailpenjualan_komoditas')
    else:
        formset = OrderFormSet(instance=penjualan_obj)
    
    return render(request, 'detailpenjualan/createdetailpenjualan_komoditas.html', {'formset': formset, 'penjualan': penjualan_obj})







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