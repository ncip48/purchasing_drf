from urllib.parse import urljoin
from django.conf import settings
from core.serializers import BaseExcludeSerializer
from purchase_request.models import PurchaseRequestDetail
from purchase_request.serializers import PurchaseRequestDetailSerializer, PurchaseRequestSerializer
from spph.models import SPPH, SPPHDetail, SPPHLampiran, SPPHVendor
from rest_framework import serializers
from vendor.serializers import VendorSerializer


# Reusable Method for Lampiran URL
def get_lampiran_url(obj):
    if obj.file:
        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8080')
        return urljoin(base_url, obj.file.url)
    return None

# Lampiran Serializer
class SPPHLampiranSerializer(BaseExcludeSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = SPPHLampiran
        fields = ['id', 'file', 'created_at']

    def get_file(self, obj):
        return get_lampiran_url(obj)

# Main SPPH Serializer
class SPPHSerializer(BaseExcludeSerializer):
    purchase_request = PurchaseRequestSerializer(read_only=True)
    vendors = VendorSerializer(many=True, read_only=True)
    lampiran = SPPHLampiranSerializer(many=True, read_only=True, source='lampiran.all')

    class Meta(BaseExcludeSerializer.Meta):
        model = SPPH

# SPPH Items Serializer with Details
class SPPHItemsSerializer(SPPHSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return SPPHDetailSerializer(obj.items.all(), many=True, context=self.context).data

# SPPH Detail Serializer
class SPPHDetailSerializer(BaseExcludeSerializer):
    purchase_request_detail = PurchaseRequestDetailSerializer(read_only=True)

    class Meta(BaseExcludeSerializer.Meta):
        model = SPPHDetail

# SPPH Detail Post Serializer
class SPPHDetailPostSerializer(BaseExcludeSerializer):
    purchase_request_detail = serializers.PrimaryKeyRelatedField(queryset=PurchaseRequestDetail.objects.all())
    spph = serializers.PrimaryKeyRelatedField(queryset=SPPH.objects.all())

    class Meta:
        model = SPPHDetail
        fields = '__all__'

# SPPH Vendor Serializer
class SPPHVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPPHVendor
        fields = ['id', 'spph', 'vendor']

# SPPH Post Serializer for Creation
class SPPHPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPPH
        fields = '__all__'
