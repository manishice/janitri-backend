from rest_framework import serializers
from apps.devices.models import Device
from apps.places.models import Place
from apps.patients.models import Patient
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

    def validate_device_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("Device ID cannot be empty.")
        if Device.objects.filter(device_id=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Device ID must be unique.")
        return value.strip()

    def validate_place(self, value):
        if not Place.objects.filter(id=value.id, is_active=True).exists():
            raise serializers.ValidationError("Place does not exist or is inactive.")
        return value

    def validate_assigned_to(self, value):
        if value:
            if not Patient.objects.filter(id=value.id).exists():
                raise serializers.ValidationError("Assigned patient does not exist.")
            # check if patient already has a device
            if Device.objects.filter(assigned_to=value).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError("This patient already has a device assigned.")
        return value
