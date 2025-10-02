from django.contrib import admin
from .models import BiodataPeserta

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
