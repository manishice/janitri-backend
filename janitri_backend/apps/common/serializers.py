from rest_framework import serializers

class StatusUpdateSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)
