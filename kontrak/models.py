import uuid
from django.db import models
from core.models import TimeStampedModel

# Create your models here.
class Kontrak(TimeStampedModel):
    class StatusChoices(models.TextChoices):
        KONTRAK = 'KONTRAK', 'Kontrak'
        KONFIRMASI_ORDER = 'KONFIRMASI_ORDER', 'Konfirmasi Order'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kode_proyek = models.CharField(max_length=20)
    tanggal = models.DateField()
    nomor = models.CharField(max_length=100)
    nama_pekerjaan = models.CharField(max_length=150)
    nilai_pekerjaan = models.BigIntegerField()
    nama_pelanggan = models.CharField(max_length=150)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.KONTRAK
    )

    def __str__(self):
        return self.nomor
    
class KontrakLampiran(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kontrak = models.ForeignKey(Kontrak, on_delete=models.CASCADE, related_name='lampiran')
    tanggal = models.DateField()
    nomor = models.CharField(max_length=100)
    perihal = models.CharField(max_length=100, null=True)
    keterangan = models.TextField(null=True)
    lampiran = models.FileField(upload_to='kontrak/lampiran/', null=True, blank=True)
    
    def __str__(self):
        return self.nomor
    
    class Meta:
        db_table = "kontrak_lampiran"
        default_permissions = ()  # Disable default permissions to avoid duplicates
        permissions = [
            ('add_kontrak_lampiran', 'Can add kontrak lampiran'),
            ('delete_kontrak_lampiran', 'Can delete kontrak lampiran'),
            ('view_kontrak_lampiran', 'Can view kontrak lampiran'),
        ]