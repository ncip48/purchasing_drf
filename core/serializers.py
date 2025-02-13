from rest_framework import serializers


class BaseExcludeSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        exclude = ['deleted_at', 'transaction_id', 'restored_at']