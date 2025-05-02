from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import Seminar, PendaftaranPeserta

def seminar_registration(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)
    
    if request.method == 'POST':
        # Cek kuota
        if seminar.pendaftaran.count() >= seminar.kuota_peserta:
            messages.error(request, "Mohon maaf, kuota peserta seminar sudah penuh.")
            return redirect(seminar.url)
        
        # Buat kode pendaftaran
        kode_pendaftaran = f"SMR-{get_random_string(8).upper()}"
        
        # Simpan data pendaftaran
        pendaftaran = PendaftaranPeserta(
            seminar=seminar,
            nama=request.POST.get('nama'),
            email=request.POST.get('email'),
            telepon=request.POST.get('telepon'),
            institusi=request.POST.get('institusi', ''),
            kode_pendaftaran=kode_pendaftaran
        )
        pendaftaran.save()
        
        # Tampilkan halaman sukses dengan kode pendaftaran
        return render(request, 'seminar/registration_success.html', {
            'pendaftaran': pendaftaran,
            'seminar': seminar
        })
    
    # Jika bukan POST request, redirect ke halaman seminar
    return redirect(seminar.url)

# Buat file seminar/urls.py untuk definisi URL
from django.urls import path
from . import views

urlpatterns = [
    path('registration/<int:seminar_id>/', views.seminar_registration, name='seminar_registration'),
]
