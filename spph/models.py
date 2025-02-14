# models.py

import uuid
from django.db import models

from core.models import TimeStampedModel
from purchase_request.models import PurchaseRequest, PurchaseRequestDetail
from vendor.models import Vendor

class SPPH(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE, related_name='spph')
    nomor_spph = models.CharField(max_length=50)
    tanggal_spph = models.DateField()
    batas_spph = models.DateField()
    perihal = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendors = models.ManyToManyField(Vendor, through='SPPHVendor')

    def __str__(self):
        return self.nomor_spph
    
class SPPHLampiran(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spph = models.ForeignKey(SPPH, on_delete=models.CASCADE, related_name="lampiran")
    file = models.FileField(upload_to='spph/lampiran/',null=True)
    
    def __str__(self):
        return self.spph.nomor_spph
    
    class Meta:
        db_table = "spph_lampiran"
        default_permissions = ()  # Disable default permissions to avoid duplicates
        permissions = [
            ('add_spph_lampiran', 'Can add SPPH lampiran'),
            ('delete_spph_lampiran', 'Can delete SPPH lampiran'),
            ('view_spph_lampiran', 'Can view SPPH lampiran'),
        ]

class SPPHVendor(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spph = models.ForeignKey(SPPH, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.spph.nomor_spph} - {self.vendor.name}"
    
    class Meta:
        db_table = "spph_vendor"
        default_permissions = ()  # Disable default permissions to avoid duplicates
        permissions = [
            ('add_spph_vendor', 'Can add SPPH vendor'),
            ('delete_spph_vendor', 'Can delete SPPH vendor'),
            ('view_spph_vendor', 'Can view SPPH vendor'),
        ]

class SPPHDetail(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spph = models.ForeignKey(SPPH, on_delete=models.CASCADE, related_name="items")
    purchase_request_detail = models.ForeignKey(PurchaseRequestDetail, on_delete=models.CASCADE)
    qty = models.IntegerField()
    
    def __str__(self):
        return self.spph.nomor_spph
    
    class Meta:
        db_table = "spph_detail"
        default_permissions = ()  # Disable default permissions to avoid duplicates
        permissions = [
            ('add_spph_detail', 'Can add SPPH detail'),
            ('delete_spph_detail', 'Can delete SPPH detail'),
            ('view_spph_detail', 'Can view SPPH detail'),
        ]