from urllib.parse import urljoin
from rest_framework import serializers
from .models import Kontrak, KontrakLampiran
from django.conf import settings


class KontrakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kontrak
        fields = '__all__'
        
class KontrakLampiranSerializer(serializers.ModelSerializer):
    lampiran = serializers.SerializerMethodField()
    
    class Meta:
        model = KontrakLampiran
        fields = '__all__'
        
    def get_lampiran(self, obj):
        if obj.lampiran:
            # Construct the absolute URL manually
            base_url = getattr(settings, 'BASE_URL', 'http://localhost:8080')
            return urljoin(base_url, obj.lampiran.url)
        return None

class KontrakDetailSerializer(serializers.ModelSerializer):
    lampiran = KontrakLampiranSerializer(many=True, read_only=True)

    class Meta:
        model = Kontrak
        fields = '__all__'