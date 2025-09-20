from rest_framework import serializers
from .models import Patient, Guardian
from apps.places.serializers import PlaceSerializer

# --------- Guardian Serializer ---------
class GuardianSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    modified_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Guardian
        fields = [
            "id",
            "name",
            "phone",
            "relation",
            "address",
            "patient",
            "created_at",
            "modified_at",
            "created_by",
            "modified_by",
        ]
        read_only_fields = ["created_at", "modified_at", "created_by", "modified_by"]

# --------- Patient Serializer ---------
class PatientSerializer(serializers.ModelSerializer):
    guardians = GuardianSerializer(many=True, read_only=True)
    place_detail = PlaceSerializer(source="place", read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    modified_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "place",
            "place_detail",
            "guardians",
            "created_at",
            "modified_at",
            "created_by",
            "modified_by",
        ]
        read_only_fields = ["created_at", "modified_at", "created_by", "modified_by"]
