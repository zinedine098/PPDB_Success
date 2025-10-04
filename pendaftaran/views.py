# pendaftaran/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm, BiodataPesertaForm
from django.contrib.auth.decorators import login_required


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
                return redirect("utama")  # arahkan ke halaman utama
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
    
# def utama(request):
#     return render(request, "pendaftaran/utama.html")
