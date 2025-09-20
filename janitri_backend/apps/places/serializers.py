from rest_framework import serializers
from .models import Place

class PlaceSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    modified_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Place
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "email",
            "is_active",
            "created_at",
            "modified_at",
            "created_by",
            "modified_by",
        ]
        read_only_fields = ["created_at", "modified_at", "created_by", "modified_by"]
