from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Page
from seminar.models import KategoriSeminar, Pembicara, Seminar, SeminarIndexPage, SeminarPembicara
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Membuat data contoh untuk sistem manajemen seminar'

    def handle(self, *args, **options):
        # Buat kategori seminar
        kategori = [
            {'nama': 'Teknologi', 'deskripsi': 'Seminar tentang perkembangan teknologi terbaru'},
            {'nama': 'Bisnis', 'deskripsi': 'Seminar tentang strategi dan pengembangan bisnis'},
            {'nama': 'Pendidikan', 'deskripsi': 'Seminar tentang inovasi pendidikan'},
        ]
        
        for k in kategori:
            KategoriSeminar.objects.get_or_create(nama=k['nama'], defaults={'deskripsi': k['deskripsi']})
        
        self.stdout.write(self.style.SUCCESS('Berhasil membuat kategori seminar'))
        
        # Buat pembicara
        pembicara = [
            {
                'nama': 'Dr. Budi Santoso',
                'email': 'budi@example.com',
                'profesi': 'Pakar Teknologi AI',
                'bio': 'Peneliti di bidang Artificial Intelligence dengan pengalaman lebih dari 10 tahun'
            },
            {
                'nama': 'Siti Aisyah, M.M.',
                'email': 'siti@example.com',
                'profesi': 'Konsultan Bisnis',
                'bio': 'Konsultan bisnis berpengalaman yang telah membantu ratusan perusahaan berkembang'
            },
            {
                'nama': 'Prof. Agus Wijaya',
                'email': 'agus@example.com',
                'profesi': 'Profesor Pendidikan',
                'bio': 'Profesor pendidikan dengan fokus pada pembelajaran digital dan inovasi kurikulum'
            },
        ]
        
        pembicara_objs = []
        for p in pembicara:
            obj, created = Pembicara.objects.get_or_create(nama=p['nama'], defaults=p)
            pembicara_objs.append(obj)
        
        self.stdout.write(self.style.SUCCESS('Berhasil membuat data pembicara'))
        
        # Cek apakah sudah ada SeminarIndexPage
        try:
            seminar_index = SeminarIndexPage.objects.get()
        except SeminarIndexPage.DoesNotExist:
            # Buat SeminarIndexPage jika belum ada
            home_page = Page.objects.get(slug='home')
            seminar_index = SeminarIndexPage(
                title='Seminar',
                intro='<p>Selamat datang di halaman seminar kami. Temukan berbagai seminar menarik di sini.</p>'
            )
            home_page.add_child(instance=seminar_index)
            seminar_index.save_revision().publish()
            
        self.stdout.write(self.style.SUCCESS('Berhasil memastikan halaman indeks seminar tersedia'))
        
        # Buat beberapa seminar contoh
        kategori_list = list(KategoriSeminar.objects.all())
        
        seminar_titles = [
            'Menguasai Teknologi AI untuk Bisnis Digital',
            'Strategi Pemasaran di Era Digital',
            'Transformasi Pendidikan dengan Teknologi Terkini',
            'Blockchain dan Aplikasinya di Industri Keuangan',
            'Pengembangan Aplikasi Mobile untuk Pemula'
        ]
        
        topik_presentasi = [
            'Pengenalan AI dalam Bisnis',
            'Machine Learning untuk Pemula',
            'Strategi Digital Marketing',
            'Teknologi Blockchain Dasar',
            'Pengembangan Aplikasi Web Modern',
            'Metode Pembelajaran Inovatif',
            'Strategi Pertumbuhan Startup'
        ]
        
        for i in range(5):
            # Tanggal acak dalam 30 hari ke depan
            tanggal = timezone.now().date() + timedelta(days=random.randint(7, 30))
            
            seminar = Seminar(
                title=seminar_titles[i],
                tanggal=tanggal,
                waktu_mulai='09:00',
                waktu_selesai='16:00',
                lokasi='Hotel Grand Indonesia, Jakarta',
                deskripsi=f'<p>Deskripsi lengkap seminar {seminar_titles[i]}. Seminar ini akan membahas berbagai topik menarik dan membawa Anda ke pemahaman mendalam tentang teknologi dan implementasinya.</p>',
                kuota_peserta=random.randint(50, 200),
                harga_tiket=random.choice([0, 50000, 100000, 150000, 200000]),
                kategori=random.choice(kategori_list)
            )
            
            seminar_index.add_child(instance=seminar)
            seminar.save_revision().publish()
            
            # Tambahkan 2 pembicara acak ke seminar
            selected_pembicara = random.sample(pembicara_objs, 2)
            for j, pembicara_obj in enumerate(selected_pembicara):
                SeminarPembicara.objects.create(
                    seminar=seminar,
                    pembicara=pembicara_obj,
                    topik_presentasi=random.choice(topik_presentasi)
                )
            
            # Publikasikan ulang dengan pembicara
            seminar.save_revision().publish()
            
        self.stdout.write(self.style.SUCCESS('Berhasil membuat data seminar contoh dengan pembicara'))