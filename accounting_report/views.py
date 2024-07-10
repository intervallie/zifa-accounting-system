import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Sum
from journal.models import Transaction


# Create your views here.
def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("user_auth:login"))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
def report_landing_page(request):
    return render(request, 'report_landing_page.html')

@login_required
def neraca_report(request, end_date):

    def get_total(code_prefix):
        return Transaction.objects.filter(
            journal_code__journal_date__lte=end_date, 
            acc_code__code__startswith=code_prefix
        ).aggregate(total=Sum('value'))['total'] or 0

    kas_total = get_total("1111")
    bank_total = get_total("1112")
    piutang_total = get_total("112")
    persediaan_total = get_total("113")
    jumlah_aset_lancar = kas_total + bank_total + piutang_total + persediaan_total

    tanah_total = get_total("121")
    kendaraan_total = get_total("122")
    peralatan_total = get_total("123")
    bangunan_total = get_total("124")
    penyusutan_total = get_total("125")
    jumlah_aset_tetap = tanah_total + kendaraan_total + peralatan_total + bangunan_total + penyusutan_total

    jumlah_aset = jumlah_aset_lancar + jumlah_aset_tetap

    utang_dagang_total = get_total("211")
    utang_saham_total = get_total("212")
    jumlah_liabilitas_pendek = utang_dagang_total + utang_saham_total

    utang_bank_total = get_total("221")
    jumlah_liabilitas_panjang = utang_bank_total

    jumlah_liabilitas = jumlah_liabilitas_pendek + jumlah_liabilitas_panjang

    modal_total = get_total("31")
    laba_total = get_total("32")
    jumlah_ekuitas = modal_total + laba_total

    jumlah_liabilitas_ekuitas = jumlah_liabilitas + jumlah_ekuitas

    list_of_report = [
        kas_total, bank_total, piutang_total, persediaan_total, jumlah_aset_lancar,
        tanah_total, kendaraan_total, peralatan_total, bangunan_total, penyusutan_total, jumlah_aset_tetap, jumlah_aset,
        utang_dagang_total, utang_saham_total, jumlah_liabilitas_pendek,
        utang_bank_total, jumlah_liabilitas_panjang, jumlah_liabilitas,
        modal_total, laba_total, jumlah_ekuitas,
        jumlah_liabilitas_ekuitas
    ]

    return render(request, 'report_neraca.html', {'list_of_report': list_of_report, 'end_date': end_date})

@login_required
def labarugi_report(request, start_date, end_date):
    
    def get_total(code_prefix):
        return Transaction.objects.filter(
            journal_code__journal_date__range=(start_date, end_date), 
            acc_code__code__startswith=code_prefix
        ).aggregate(total=Sum('value'))['total'] or 0

    penjualan = get_total("41")
    harga_pokok_penjualan = get_total("62")
    laba_kotor = penjualan - harga_pokok_penjualan

    beban_1 = get_total("51")
    beban_2 = get_total("52")
    beban_3 = get_total("53")
    laba_sebelum_pajak = laba_kotor - (beban_1 + beban_2 + beban_3)


    list_of_report = [
        penjualan, harga_pokok_penjualan, laba_kotor,
        beban_1, beban_2, beban_3, laba_sebelum_pajak
    ]

    return render(request, 'report_laba_rugi.html', {
        'list_of_report': list_of_report, 
        'start_date': start_date, 
        'end_date': end_date
    })

