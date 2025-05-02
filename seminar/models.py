from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable
from modelcluster.models import ClusterableModel

# Model untuk kategori seminar
class KategoriSeminar(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)

    panels = [
        FieldPanel('nama'),
        FieldPanel('deskripsi'),
    ]

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Kategori Seminar"
        verbose_name_plural = "Kategori Seminar"

# Model untuk pembicara
class Pembicara(models.Model):
    nama = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    profesi = models.CharField(max_length=100, blank=True)
    bio = RichTextField(blank=True)
    foto = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('nama'),
        FieldPanel('email'),
        FieldPanel('profesi'),
        FieldPanel('bio'),
        FieldPanel('foto'),
    ]

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Pembicara"
        verbose_name_plural = "Pembicara"

# Model untuk seminar
class Seminar(Page):
    template = "seminar/seminar_page.html"
    tanggal = models.DateField("Tanggal Seminar")
    waktu_mulai = models.TimeField("Waktu Mulai")
    waktu_selesai = models.TimeField("Waktu Selesai")
    lokasi = models.CharField(max_length=255)
    deskripsi = RichTextField(blank=True)
    kuota_peserta = models.PositiveIntegerField(default=100)
    harga_tiket = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gambar_utama = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    kategori = models.ForeignKey(
        KategoriSeminar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='seminar'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('tanggal'),
        FieldPanel('waktu_mulai'),
        FieldPanel('waktu_selesai'),
        FieldPanel('lokasi'),
        FieldPanel('deskripsi'),
        FieldPanel('kategori'),
        MultiFieldPanel([
            FieldPanel('kuota_peserta'),
            FieldPanel('harga_tiket'),
        ], heading="Informasi Tiket"),
        FieldPanel('gambar_utama'),
        InlinePanel('pembicara_seminar', label="Pembicara"),
    ]
    
    parent_page_types = ['SeminarIndexPage']
    subpage_types = []
    
    search_fields = Page.search_fields + [
        index.SearchField('deskripsi'),
        index.FilterField('tanggal'),
    ]

# Model untuk Pembicara Seminar (hubungan many-to-many)
class SeminarPembicara(Orderable):
    seminar = ParentalKey('Seminar', on_delete=models.CASCADE, related_name='pembicara_seminar')
    pembicara = models.ForeignKey(
        'Pembicara',
        on_delete=models.CASCADE,
        related_name='seminar_pembicara'
    )
    topik_presentasi = models.CharField(max_length=255, blank=True)
    
    panels = [
        FieldPanel('pembicara'),
        FieldPanel('topik_presentasi'),
    ]

# Model untuk Pendaftaran Peserta
class PendaftaranPeserta(models.Model):
    seminar = models.ForeignKey(
        Seminar,
        on_delete=models.CASCADE,
        related_name='pendaftaran'
    )
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    telepon = models.CharField(max_length=20)
    institusi = models.CharField(max_length=100, blank=True)
    tanggal_daftar = models.DateTimeField(default=timezone.now)
    status_pembayaran = models.BooleanField(default=False)
    kode_pendaftaran = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.nama} - {self.seminar.title}"
    
    class Meta:
        verbose_name = "Pendaftaran Peserta"
        verbose_name_plural = "Pendaftaran Peserta"

# Halaman indeks untuk menampilkan daftar seminar
class SeminarIndexPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
    subpage_types = ['Seminar']
    
    def get_context(self, request):
        context = super().get_context(request)
        seminar_list = Seminar.objects.child_of(self).live().order_by('-tanggal')
        context['seminar_list'] = seminar_list
        return context