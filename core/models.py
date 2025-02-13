from django.db import models
from django_softdelete.models import SoftDeleteModel

class TimeStampedModel(SoftDeleteModel):
    """Abstract base class that adds created_at and updated_at fields to models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True