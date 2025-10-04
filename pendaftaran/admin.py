from django.contrib import admin
from .models import BiodataPeserta
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import BerkasSiswa

@admin.register(BiodataPeserta)
class BiodataPesertaAdmin(admin.ModelAdmin):
    list_display = (
        'nama_lengkap',
        'nik',
        'nomor_kk',
        'jenis_kelamin',
        'tanggal_lahir',
        'jurusan',
        'ukuran_seragam',
        'user'
    )
    search_fields = (
        'nama_lengkap',
        'nik',
        'nomor_kk',
        'user__username',
        'user__email'
    )
    list_filter = (
        'jenis_kelamin',
        'jurusan',
        'provinsi',
        'kabupaten'
    )
    ordering = ('nama_lengkap',)


# apps/berkas/admin.py


# Mendefinisikan kelas admin kustom untuk model BerkasSiswa
@admin.register(BerkasSiswa)
class BerkasSiswaAdmin(admin.ModelAdmin):
    """
    Konfigurasi tampilan model BerkasSiswa di halaman admin Django.
    """
    # Field yang akan ditampilkan di halaman daftar (list view)
    list_display = (
        'get_user_full_name', 
        'get_user_username', 
        'all_files_uploaded'
    )

    # Field yang bisa digunakan untuk pencarian
    search_fields = (
        'user__username', 
        'user__first_name', 
        'user__last_name'
    )

    # Field yang akan menjadi link ke halaman detail
    list_display_links = ('get_user_full_name',)

    # Field yang tidak bisa diubah di halaman detail
    readonly_fields = ('user',)

    # Mengelompokkan field untuk tampilan yang lebih rapi di form input
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Data Pribadi', {
            'fields': ('foto_profile',)
        }),
        ('Dokumen Pendidikan', {
            'fields': ('surat_keterangan_lulus', 'ijazah')
        }),
        ('Dokumen Keluarga', {
            'fields': ('ktp_orang_tua_lk', 'ktp_orang_tua_pr', 'foto_kk', 'foto_akte_kelahiran')
        }),
    )

    # --- Metode Kustom untuk Tampilan ---

    @admin.display(description="Nama Lengkap Siswa", ordering='user__last_name')
    def get_user_full_name(self, obj):
        """Menampilkan nama lengkap user jika ada, jika tidak ada tampilkan username."""
        full_name = obj.user.get_full_name()
        return full_name if full_name else obj.user.username

    @admin.display(description="Username", ordering='user__username')
    def get_user_username(self, obj):
        """Menampilkan username user."""
        return obj.user.username

    @admin.display(description="Status Upload", boolean=True)
    def all_files_uploaded(self, obj):
        """
        Menampilkan ikon centang (True) atau silang (False) apakah semua file sudah diunggah.
        """
        required_fields = [
            obj.foto_profile, obj.surat_keterangan_lulus, obj.ijazah,
            obj.ktp_orang_tua_lk, obj.ktp_orang_tua_pr, obj.foto_kk, obj.foto_akte_kelahiran
        ]
        # Cek apakah semua field memiliki file (tidak kosong)
        return all(field for field in required_fields)


# --- BONUS: Mengelola Berkas Langsung dari Halaman User ---

# Definisikan Inline untuk BerkasSiswa
class BerkasSiswaInline(admin.StackedInline):
    """
    Menampilkan form BerkasSiswa di dalam halaman edit User.
    """
    model = BerkasSiswa
    can_delete = False
    verbose_name_plural = 'Berkas Siswa'
    # Gunakan fieldsets yang sama untuk konsistensi
    fieldsets = (
        ('Data Pribadi', {
            'fields': ('foto_profile',)
        }),
        ('Dokumen Pendidikan', {
            'fields': ('surat_keterangan_lulus', 'ijazah')
        }),
        ('Dokumen Keluarga', {
            'fields': ('ktp_orang_tua_lk', 'ktp_orang_tua_pr', 'foto_kk', 'foto_akte_kelahiran')
        }),
    )


# Perluas kelas UserAdmin bawaan Django
class UserAdmin(BaseUserAdmin):
    inlines = (BerkasSiswaInline,)

# Hapus pendaftaran UserAdmin bawaan dan daftarkan yang baru
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
