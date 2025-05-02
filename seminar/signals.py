from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PendaftaranPeserta
import random
import string

@receiver(pre_save, sender=PendaftaranPeserta)
def create_registration_code(sender, instance, **kwargs):
    if not instance.kode_pendaftaran:
        # Buat kode pendaftaran acak
        chars = string.ascii_uppercase + string.digits
        kode = ''.join(random.choice(chars) for _ in range(8))
        instance.kode_pendaftaran = f"SMR-{kode}"
