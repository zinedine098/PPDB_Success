from django.db import models
from django.contrib.auth.models import User

class BiodataPeserta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Biodata
    kewarganegaraan = models.CharField(max_length=50)
    nomor_kk = models.CharField(max_length=20, unique=True)
    nik = models.CharField(max_length=20, unique=True)
    nama_lengkap = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(
        max_length=10,
        choices=(('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan'))
    )
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    anak_ke = models.IntegerField()
    pendidikan_terakhir = models.CharField(max_length=50)

    # Alamat
    negara = models.CharField(max_length=50)
    provinsi = models.CharField(max_length=50)
    kabupaten = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    jalan = models.CharField(max_length=100)
    kode_pos = models.CharField(max_length=10)

    # Rencana Pendidikan
    # jurusan = models.CharField(max_length=100)
    jurusan = models.CharField(
        max_length=30,
        choices=(('Rekayasa Perangkat Lunak', 'Rekayasa Perangkat Lunak'), ('MultiMedia', 'MultiMedia'), ('Teknik Komputer Jaringan', 'Teknik Komputer Jaringan'))
    )
    ukuran_seragam = models.CharField(max_length=10)

    def __str__(self):
        return self.nama_lengkap
