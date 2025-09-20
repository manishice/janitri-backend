from rest_framework import serializers
from .models import Place
from apps.common.validators import phone_validator

class PlaceSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, validators=[phone_validator])
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
        
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Place name cannot be empty.")
        return value.strip()

    def validate_email(self, value):
        if value:
            return value.strip().lower()
        return value

    def validate_address(self, value):
        if value:
            return value.strip()
        return value
