from core.serializers import BaseExcludeSerializer
from purchase_request.serializers import PurchaseRequestSerializer
from spph.models import SPPH
from rest_framework import serializers
from vendor.serializers import VendorSerializer


class SPPHSerializer(BaseExcludeSerializer):
    purchase_request = PurchaseRequestSerializer(read_only=True)
    vendors = VendorSerializer(many=True, read_only=True)

    class Meta(BaseExcludeSerializer.Meta):
        model = SPPH
        
class SPPHDetailSerializer(BaseExcludeSerializer):
    purchase_request = PurchaseRequestSerializer(read_only=True)
    vendors = VendorSerializer(many=True, read_only=True)

    class Meta:
        model = SPPH
        fields = '__all__'

class SPPHPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPPH
        fields = '__all__'
