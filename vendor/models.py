import uuid
from django.db import models

from core.models import TimeStampedModel

# Create your models here.
class Vendor(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    alamat = models.TextField()
    telp = models.CharField(max_length=50, null=True)
    fax = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    
    def __str__(self):
        return self.nama
