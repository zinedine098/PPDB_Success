# pendaftaran/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm, BiodataPesertaForm
from django.contrib.auth.decorators import login_required
from .forms import BerkasSiswaForm
from .models import BerkasSiswa, BiodataPeserta

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        biodata_form = BiodataPesertaForm(request.POST)
        
        # Debug: print form errors
        if not user_form.is_valid():
            print("User Form Errors:", user_form.errors)
        
        if not biodata_form.is_valid():
            print("Biodata Form Errors:", biodata_form.errors)
        
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

@never_cache
def logout_user(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    # Ambil objek user yang sedang login
    user = request.user
    
    # Inisialisasi variabel biodata dan berkas menjadi None
    # Ini untuk mencegah error jika data belum ada
    biodata = None
    berkas = None
    
    # Coba ambil data BiodataPeserta yang terkait dengan user
    try:
        # Django secara otomatis membuat relasi terbalik.
        # Nama relasinya adalah nama model (lowercase), yaitu 'biodatapeserta'
        biodata = user.biodatapeserta
    except BiodataPeserta.DoesNotExist:
        # Jika data tidak ditemukan, biarkan variabel biodata tetap None
        pass

    # Coba ambil data BerkasSiswa yang terkait dengan user
    try:
        # Karena di model BerkasSiswa kita menggunakan related_name='berkas_siswa',
        # kita bisa mengaksesnya dengan nama tersebut.
        berkas = user.berkas_siswa
    except BerkasSiswa.DoesNotExist:
        # Jika data tidak ditemukan, biarkan variabel berkas tetap None
        pass

    # Siapkan context untuk dikirim ke template
    context = {
        'biodata': biodata,
        'berkas': berkas,
    }
    
    # Render template dengan context yang sudah disiapkan
    return render(request, "pendaftaran/home.html", context)
@login_required
def upload_berkas(request):
    """
    View untuk menampilkan dan memproses form pengunggahan berkas siswa.
    Hanya pengguna yang login yang dapat mengakses halaman ini.
    Jika pengguna sudah pernah mengunggah berkas, mereka akan diarahkan ke halaman 'home'.
    """
    # Cek apakah pengguna sudah memiliki objek BerkasSiswa
    try:
        # Jika objek ditemukan, artinya user sudah pernah upload
        berkas_instance = request.user.berkas_siswa
        # Langsung arahkan ke halaman 'home'
        return redirect('home')
    except BerkasSiswa.DoesNotExist:
        # Jika objek tidak ditemukan, biarkan berkas_instance tetap None
        # dan lanjutkan untuk menampilkan form.
        berkas_instance = None

    # Kode di bawah ini hanya akan dijalankan jika user BELUM pernah upload
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
        # Jika adalah request GET, tampilkan form kosong
        form = BerkasSiswaForm(instance=berkas_instance)

    # Render template dengan form
    return render(request, 'pendaftaran/berkas.html', {'form': form})
def sukses_upload(request):
    """
    View sederhana untuk menampilkan halaman sukses.
    """
    return render(request, 'pendaftaran/sukses.html')

def ubah_berkas(request):
    """
    View sederhana untuk menampilkan halaman sukses.
    """
    return render(request, 'pendaftaran/ubahberkas.html')
# views.py
def profile(request):
    user = request.user
    biodata = None
    berkas = None
    
    try:
        biodata = user.biodatapeserta
    except BiodataPeserta.DoesNotExist:
        pass

    try:
        berkas = user.berkas_siswa
    except BerkasSiswa.DoesNotExist:
        pass

    # --- TAMBAHKAN BARIS INI UNTUK DEBUGGING ---

    # -------------------------------------------

    context = {
        'biodata': biodata,
        'berkas': berkas,
    }

    return render(request, 'pendaftaran/profile.html', context)
