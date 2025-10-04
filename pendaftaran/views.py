# pendaftaran/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm, BiodataPesertaForm
from django.contrib.auth.decorators import login_required
from .forms import BerkasSiswaForm
from .models import BerkasSiswa

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        biodata_form = BiodataPesertaForm(request.POST)
        if user_form.is_valid() and biodata_form.is_valid():
            # Simpan user dulu
            user = user_form.save()
            # Simpan biodata dan kaitkan dengan user
            biodata = biodata_form.save(commit=False)
            biodata.user = user
            biodata.save()
            messages.success(request, "Pendaftaran berhasil! Silakan login.")
            return redirect('login')
        else:
            messages.error(request, "Terjadi kesalahan. Silakan periksa kembali data yang Anda masukkan.")
    else:
        user_form = UserRegisterForm()
        biodata_form = BiodataPesertaForm()

    context = {
        'user_form': user_form,
        'biodata_form': biodata_form
    }
    return render(request, 'pendaftaran/register.html', context)

# pendaftaran/views.py

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("upload_berkas")  # arahkan ke halaman berkas
    else:
        form = AuthenticationForm()
    return render(request, "pendaftaran/login.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
@never_cache
def home(request):
    return render(request, "pendaftaran/home.html")

@login_required
def upload_berkas(request):
    """
    View untuk menampilkan dan memproses form pengunggahan berkas siswa.
    Hanya pengguna yang login yang dapat mengakses halaman ini.
    """
    # Cek apakah pengguna sudah memiliki objek BerkasSiswa
    try:
        berkas_instance = request.user.berkas_siswa
    except BerkasSiswa.DoesNotExist:
        berkas_instance = None

    if request.method == 'POST':
        # Jika form disubmit, proses data POST dan FILES
        form = BerkasSiswaForm(request.POST, request.FILES, instance=berkas_instance)
        if form.is_valid():
            # Simpan objek form, tapi jangan commit ke database dulu
            berkas_obj = form.save(commit=False)
            # Hubungkan dengan user yang sedang login
            berkas_obj.user = request.user
            # Sekarang, simpan ke database
            berkas_obj.save()
            # Redirect ke halaman sukses atau halaman lain
            return redirect('sukses_upload') # Ganti dengan nama URL sukses Anda
    else:
        # Jika adalah request GET, tampilkan form kosong atau form dengan data yang sudah ada
        form = BerkasSiswaForm(instance=berkas_instance)

    # Render template dengan form
    return render(request, 'pendaftaran/berkas.html', {'form': form})

def sukses_upload(request):
    """
    View sederhana untuk menampilkan halaman sukses.
    """
    return render(request, 'pendaftaran/sukses.html')
