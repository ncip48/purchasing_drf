# serializers.py

from core.serializers import BaseExcludeSerializer
from kontrak.models import Kontrak
from rest_framework import serializers
from users.serializers import UserProfileSerializer
from .models import PurchaseRequest, PurchaseRequestDetail
from kontrak.serializers import KontrakSerializer

class PurchaseRequestPostSerializer(serializers.ModelSerializer):
    kontrak = serializers.PrimaryKeyRelatedField(queryset=Kontrak.objects.all())

    class Meta:
        model = PurchaseRequest
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        # You can customize the creation logic if needed
        return super().create(validated_data)

class PurchaseRequestSerializer(BaseExcludeSerializer):
    user = UserProfileSerializer(read_only=True)
    kontrak = KontrakSerializer(read_only=True)

    class Meta(BaseExcludeSerializer.Meta):
        model = PurchaseRequest

class PurchaseRequestItemsSerializer(PurchaseRequestSerializer):
    items = serializers.SerializerMethodField()

    class Meta(PurchaseRequestSerializer.Meta):
        pass

    def get_items(self, obj):
        return PurchaseRequestDetailSerializer(obj.items.all(), many=True, context=self.context).data

class PurchaseRequestDetailSerializer(BaseExcludeSerializer):
    class Meta(BaseExcludeSerializer.Meta):
        model = PurchaseRequestDetail
        exclude = ['purchase_request', 'deleted_at', 'transaction_id', 'restored_at']

class PurchaseRequestDetailPostSerializer(serializers.ModelSerializer):
    purchase_request = serializers.PrimaryKeyRelatedField(queryset=PurchaseRequest.objects.all())

    class Meta:
        model = PurchaseRequestDetail
        fields = '__all__'
