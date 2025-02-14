from core.serializers import BaseExcludeSerializer
from .models import Vendor

class VendorSerializer(BaseExcludeSerializer):
    class Meta(BaseExcludeSerializer.Meta):
        model = Vendor