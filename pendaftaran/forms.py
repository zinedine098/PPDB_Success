# forms.py

from .models import BerkasSiswa
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BiodataPeserta

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan email anda'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Konfirmasi password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BiodataPesertaForm(forms.ModelForm):
    tanggal_lahir = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Override fields untuk menambahkan class Bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'tanggal_lahir':  # tanggal_lahir sudah diatur di atas
                if isinstance(field, forms.CharField):
                    field.widget.attrs.update({
                        'class': 'form-control',
                        'placeholder': f'Masukkan {self.Meta.model._meta.get_field(field_name).verbose_name}'
                    })
                elif isinstance(field, forms.ChoiceField):
                    field.widget.attrs.update({'class': 'form-select'})
                elif isinstance(field, forms.IntegerField):
                    field.widget.attrs.update({
                        'class': 'form-control',
                        'placeholder': f'Masukkan {self.Meta.model._meta.get_field(field_name).verbose_name}'
                    })

    class Meta:
        model = BiodataPeserta
        # --- PERUBAHAN ADA DI BARIS INI ---
        # Tambahkan 'status' ke dalam exclude agar tidak muncul di form
        exclude = ['user', 'status']
        # ---------------------------------
        labels = {
            'kewarganegaraan': 'Kewarganegaraan',
            'nomor_kk': 'Nomor Kartu Keluarga',
            'nik': 'NIK',
            'nama_lengkap': 'Nama Lengkap',
            'jenis_kelamin': 'Jenis Kelamin',
            'tempat_lahir': 'Tempat Lahir',
            'tanggal_lahir': 'Tanggal Lahir',
            'anak_ke': 'Anak Ke-',
            'pendidikan_terakhir': 'Pendidikan Terakhir',
            'negara': 'Negara',
            'provinsi': 'Provinsi',
            'kabupaten': 'Kabupaten/Kota',
            'kecamatan': 'Kecamatan',
            'jalan': 'Jalan',
            'kode_pos': 'Kode Pos',
            'jurusan': 'Jurusan yang Dipilih',
            'ukuran_seragam': 'Ukuran Seragam',
        }

# berkas siswa form

class BerkasSiswaForm(forms.ModelForm):
    """
    Form untuk mengupload dan mengelola berkas-berkas siswa.
    Form ini secara otomatis mengaitkan data dengan pengguna yang sedang login.
    """
    class Meta:
        model = BerkasSiswa
        # Exclude field 'user' karena akan diisi otomatis dari request.user
        exclude = ['user']
        # Anda bisa menentukan fields secara eksplisit jika lebih suka
        # fields = [
        #     'foto_profile', 'surat_keterangan_lulus', 'ijazah', 
        #     'ktp_orang_tua_lk', 'ktp_orang_tua_pr', 'foto_kk', 
        #     'foto_akte_kelahiran'
        # ]

    def __init__(self, *args, **kwargs):
        """
        Override __init__ untuk menambahkan kelas CSS dan atribut lain
        pada setiap field, sehingga lebih mudah di-styling di frontend.
        """
        super().__init__(*args, **kwargs)
        # Tambahkan kelas 'form-control' Bootstrap ke semua field
        for field_name, field in self.fields.items():
            # Untuk field file (ImageField), gunakan ClearableFileInput
            if isinstance(field, forms.ImageField):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'accept': 'image/*' # Membantu memfilter file di file browser
                })
            # Anda bisa menambahkan tipe field lain jika perlu
            # elif isinstance(field, forms.CharField):
            #     field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        """
        Validasi tingkat form. Digunakan untuk memeriksa aturan yang melibatkan
        beberapa field atau validasi kustom yang tidak spesifik ke satu field.
        Di sini, kita akan menambahkan validasi ukuran file.
        """
        cleaned_data = super().clean()
        MAX_FILE_SIZE = 5 * 1024 * 1024  # Batas ukuran file: 5MB

        # Iterasi melalui semua field di form
        for field_name, field in self.fields.items():
            # Pastikan field tersebut adalah ImageField
            if isinstance(field, forms.ImageField):
                file = cleaned_data.get(field_name)
                if file:
                    if file.size > MAX_FILE_SIZE:
                        # Tambahkan error ke field spesifik jika file terlalu besar
                        self.add_error(
                            field_name, 
                            f"Ukuran file untuk '{field.label}' tidak boleh lebih dari 5MB."
                        )
        return cleaned_data