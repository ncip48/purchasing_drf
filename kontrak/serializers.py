from urllib.parse import urljoin
from core.serializers import BaseExcludeSerializer
from rest_framework import serializers
from django.conf import settings
from .models import Kontrak, KontrakLampiran


class KontrakSerializer(BaseExcludeSerializer):
    class Meta(BaseExcludeSerializer.Meta):
        model = Kontrak


class KontrakDetailSerializer(KontrakSerializer):
    lampirans = serializers.SerializerMethodField()

    class Meta(KontrakSerializer.Meta):
        pass

    def get_lampirans(self, obj):
        lampirans = obj.lampirans.all()
        return KontrakLampiranReadSerializer(lampirans, many=True, context=self.context).data


class KontrakLampiranSerializer(BaseExcludeSerializer):
    class Meta(BaseExcludeSerializer.Meta):
        model = KontrakLampiran


class KontrakLampiranReadSerializer(serializers.ModelSerializer):
    lampiran = serializers.SerializerMethodField()

    class Meta:
        model = KontrakLampiran
        fields = ['id', 'lampiran', 'tanggal', 'nomor', 'perihal', 'keterangan', 'created_at']

    def get_lampiran(self, obj):
        if obj.lampiran:
            base_url = getattr(settings, 'BASE_URL', 'http://localhost:8080')
            return urljoin(base_url, obj.lampiran.url)
        return None
