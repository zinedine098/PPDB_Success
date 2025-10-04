from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
    ukuran_seragam = models.CharField(
        max_length=5,
        choices=(('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL'))
    )

    def __str__(self):
        return self.nama_lengkap

class BerkasSiswa(models.Model):
    """
    Model ini menyimpan berbagai berkas penting seorang siswa.
    Setiap instance dari model ini terhubung OneToOneField dengan model User.
    Semua field berkas pada model ini WAJIB diisi.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='berkas_siswa')

    # Field untuk menyimpan berkas-berkas siswa (sekarang WAJIB)
    foto_profile = models.ImageField(
        upload_to='berkas_siswa/foto_profile/', 
        verbose_name="Foto Profil"
    )
    surat_keterangan_lulus = models.ImageField(
        upload_to='berkas_siswa/surat_keterangan_lulus/', 
        verbose_name="Surat Keterangan Lulus"
    )
    ijazah = models.ImageField(
        upload_to='berkas_siswa/ijazah/', 
        verbose_name="Ijazah"
    )
    ktp_orang_tua_lk = models.ImageField(
        upload_to='berkas_siswa/ktp_ayah/', 
        verbose_name="KTP Ayah"
    )
    ktp_orang_tua_pr = models.ImageField(
        upload_to='berkas_siswa/ktp_ibu/', 
        verbose_name="KTP Ibu"
    )
    foto_kk = models.ImageField(
        upload_to='berkas_siswa/foto_kk/', 
        verbose_name="Foto Kartu Keluarga (KK)"
    )
    foto_akte_kelahiran = models.ImageField(
        upload_to='berkas_siswa/foto_akte_kelahiran/', 
        verbose_name="Foto Akte Kelahiran"
    )

    class Meta:
        verbose_name = "Berkas Siswa"
        verbose_name_plural = "Data Berkas Siswa"

    def __str__(self):
        return f"Berkas dari {self.user.username}"