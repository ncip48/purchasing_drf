import uuid
from django.db import models
from core.models import TimeStampedModel
from kontrak.models import Kontrak
from users.models import User

# Create your models here.
class PurchaseRequest(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kontrak = models.ForeignKey(Kontrak, on_delete=models.CASCADE)
    nomor = models.CharField(max_length=100)
    tanggal = models.DateField()
    
    def __str__(self):
        return self.nomor

    class Meta:
        db_table = "purchase_request"
        default_permissions = ()  # Disable default permissions to avoid duplicates
        permissions = [
            ('add_purchase_request', 'Can add purchase request'),
            ('change_purchase_request', 'Can change purchase request'),
            ('delete_purchase_request', 'Can delete purchase request'),
            ('view_purchase_request', 'Can view purchase request'),
        ]
    
class PurchaseRequestDetail(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name="items")
    kode_material = models.CharField(max_length=100)
    nama_barang = models.CharField(max_length=200)
    spesifikasi = models.CharField(max_length=200)
    qty = models.IntegerField()
    satuan = models.CharField(max_length=10)
    waktu_penyelesaian = models.DateField()
    lampiran = models.FileField(upload_to='kontrak/purchase_request/', null=True, blank=True)
    keterangan = models.TextField(null=True)
    
    def __str__(self):
        return self.kode_material
    
    class Meta:
        db_table = "purchase_request_detail"
        default_permissions = ()  # Disable default permissions to avoid duplicates
        permissions = [
            ('add_purchase_request_detail', 'Can add purchase request detail'),
            ('change_purchase_request_detail', 'Can change purchase request detail'),
            ('delete_purchase_request_detail', 'Can delete purchase request detail'),
            ('view_purchase_request_detail', 'Can view purchase request detail'),
        ]
    
    
