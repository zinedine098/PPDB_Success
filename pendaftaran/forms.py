# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from .models import BiodataPeserta

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# class BiodataPesertaForm(forms.ModelForm):
#     class Meta:
#         model = BiodataPeserta
#         exclude = ['user']


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
        exclude = ['user']
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