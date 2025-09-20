from rest_framework import serializers
from .models import Device
from apps.places.serializers import PlaceSerializer
from apps.patients.serializers import PatientSerializer

class DeviceSerializer(serializers.ModelSerializer):
    place_detail = PlaceSerializer(source="place", read_only=True)
    assigned_to_detail = PatientSerializer(source="assigned_to", read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    modified_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Device
        fields = [
            "id",
            "device_id",
            "place",
            "place_detail",
            "assigned_to",
            "assigned_to_detail",
            "is_active",
            "created_at",
            "modified_at",
            "created_by",
            "modified_by",
        ]
        read_only_fields = ["created_at", "modified_at", "created_by", "modified_by"]
