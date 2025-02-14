from urllib.parse import urljoin
from core.serializers import BaseExcludeSerializer
from purchase_request.models import PurchaseRequestDetail
from purchase_request.serializers import PurchaseRequestDetailSerializer, PurchaseRequestSerializer
from spph.models import SPPH, SPPHDetail, SPPHLampiran
from rest_framework import serializers
from vendor.serializers import VendorSerializer
from django.conf import settings

class SPPHSerializer(BaseExcludeSerializer):
    purchase_request = PurchaseRequestSerializer(read_only=True)
    vendors = VendorSerializer(many=True, read_only=True)
    lampiran = serializers.SerializerMethodField()

    class Meta(BaseExcludeSerializer.Meta):
        model = SPPH
        
    def get_lampiran(self, obj):
        lampiran = obj.lampiran.all()
        return SPPHLampiranReadSerializer(lampiran, many=True, context=self.context).data
        
class SPPHItemsSerializer(BaseExcludeSerializer):
    purchase_request = PurchaseRequestSerializer(read_only=True)
    items = serializers.SerializerMethodField()
    vendors = VendorSerializer(many=True, read_only=True)
    lampiran = serializers.SerializerMethodField()

    class Meta(BaseExcludeSerializer.Meta):
        model = SPPH
        
    def get_items(self, obj):
        detail = obj.items.all()
        return SPPHDetailSerializer(detail, many=True, context=self.context).data
    
    def get_lampiran(self, obj):
        lampiran = obj.lampiran.all()
        return SPPHLampiranReadSerializer(lampiran, many=True, context=self.context).data

class SPPHLampiranSerializer(BaseExcludeSerializer):
    class Meta(BaseExcludeSerializer.Meta):
        model = SPPHLampiran
        
class SPPHLampiranReadSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = SPPHLampiran
        fields = ['id', 'file', 'created_at']

    def get_file(self, obj):
        if obj.file:
            base_url = getattr(settings, 'BASE_URL', 'http://localhost:8080')
            return urljoin(base_url, obj.file.url)
        return None
    
class SPPHPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPPH
        fields = '__all__'
        
class SPPHDetailSerializer(BaseExcludeSerializer):
    purchase_request_detail = PurchaseRequestDetailSerializer(read_only=True)
    # spph = SPPHSerializer(read_only=True)
    class Meta(BaseExcludeSerializer.Meta):
        model = SPPHDetail


class SPPHDetailPostSerializer(BaseExcludeSerializer):
    purchase_request_detail = serializers.PrimaryKeyRelatedField(queryset=PurchaseRequestDetail.objects.all())
    spph = serializers.PrimaryKeyRelatedField(queryset=SPPH.objects.all())

    class Meta:
        model = SPPHDetail
        fields = '__all__'