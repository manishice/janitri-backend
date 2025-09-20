from rest_framework import serializers
from .models import Patient, Guardian
from apps.places.serializers import PlaceSerializer
from apps.common.validators import phone_validator
from utils.constants.choices import GENDER_CHOICES, RELATION_CHOICES
# --------- Guardian Serializer ---------


class GuardianSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    modified_by = serializers.StringRelatedField(read_only=True)
    phone = serializers.CharField(validators=[phone_validator])

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

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Guardian name cannot be empty.")
        return value.strip().title()  # capitalize properly

    def validate_relation(self, value):
        allowed_relations = [choice[0] for choice in RELATION_CHOICES]
        if value not in allowed_relations:
            raise serializers.ValidationError(f"Relation must be one of {allowed_relations}.")
        return value

    def validate_address(self, value):
        if value:
            return value.strip()
        return value


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

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Patient name cannot be empty.")
        return value.strip().title()

    def validate_age(self, value):
        if value <= 0:
            raise serializers.ValidationError("Age must be greater than zero.")
        return value

    def validate_gender(self, value):
        allowed_genders = [choice[0] for choice in GENDER_CHOICES]
        if value not in allowed_genders:
            raise serializers.ValidationError(f"Gender must be one of {allowed_genders}.")
        return value

    def validate_place(self, value):
        from apps.places.models import Place
        if not Place.objects.filter(id=value.id, is_active=True).exists():
            raise serializers.ValidationError("Place does not exist or is inactive.")
        return value
