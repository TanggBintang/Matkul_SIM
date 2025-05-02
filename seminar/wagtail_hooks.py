from wagtail import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from wagtail.admin.site_summary import SummaryItem
from django.utils.html import format_html
from django.templatetags.static import static
from django.utils import timezone
from django.utils.safestring import mark_safe

from seminar.models import Seminar, Pembicara, KategoriSeminar, PendaftaranPeserta

# ========================
# Statistik Dashboard Admin
# ========================
@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/seminar-admin.css'))

class SeminarStatsPanel(SummaryItem):
    order = 50
    template_name = 'seminar/admin/dashboard_stats.html'

    def __init__(self, request):
        super().__init__(request)

    def get_context(self):
        context = super().get_context()

        seminar_count = Seminar.objects.live().count()
        upcoming_seminars = Seminar.objects.live().filter(tanggal__gte=timezone.now().date()).count()
        total_registrations = PendaftaranPeserta.objects.count()
        paid_registrations = PendaftaranPeserta.objects.filter(status_pembayaran=True).count()

        context.update({
            'seminar_count': seminar_count,
            'upcoming_seminars': upcoming_seminars,
            'total_registrations': total_registrations,
            'paid_registrations': paid_registrations,
        })

        return context

@hooks.register('construct_homepage_summary_items')
def add_seminar_stats_summary_item(request, items):
    items.append(SeminarStatsPanel(request))


# ========================
# Admin Menu: Manajemen Seminar
# ========================
class KategoriSeminarAdmin(ModelAdmin):
    model = KategoriSeminar
    menu_label = 'Kategori Seminar'
    menu_icon = 'tag'
    list_display = ('nama', 'deskripsi')
    search_fields = ('nama',)

class PembicaraAdmin(ModelAdmin):
    model = Pembicara
    menu_label = 'Pembicara'
    menu_icon = 'user'
    list_display = ('nama', 'profesi', 'email')
    search_fields = ('nama', 'profesi')

class PendaftaranPesertaAdmin(ModelAdmin):
    model = PendaftaranPeserta
    menu_label = 'Pendaftaran Peserta'
    menu_icon = 'form'
    list_display = ('nama', 'email', 'seminar', 'tanggal_daftar', 'status_pembayaran')
    list_filter = ('seminar', 'status_pembayaran')
    search_fields = ('nama', 'email', 'kode_pendaftaran')

class SeminarAdminGroup(ModelAdminGroup):
    menu_label = 'Manajemen Seminar'
    menu_icon = 'date'
    menu_order = 200
    items = (KategoriSeminarAdmin, PembicaraAdmin, PendaftaranPesertaAdmin)

modeladmin_register(SeminarAdminGroup)
