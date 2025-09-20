from rest_framework import serializers
from django.core.validators import RegexValidator
from apps.users.models import User, UserManager
from apps.places.models import Place
from apps.common.validators import phone_validator
from utils.constants.choices import ROLE_CHOICES


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, validators=[phone_validator])

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name",
            "phone", "address", "role", "is_active",
            "created_at", "modified_at"
        ]
        read_only_fields = ["id", "role", "created_at", "modified_at"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(required=False, validators=[phone_validator])

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "phone", "address"]
        
    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        return value.strip().capitalize()

    def validate_last_name(self, value):
        if value:
            return value.strip().capitalize()
        return value


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AdminCreateUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, validators=[phone_validator])

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "address", "role", "place"]
    
    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        return value.strip().capitalize()

    def validate_last_name(self, value):
        if value:
            return value.strip().capitalize()
        return value

    def validate_role(self, value):
        allowed_roles = [choice[0] for choice in ROLE_CHOICES]
        if value not in allowed_roles:
            raise serializers.ValidationError(f"Role must be one of {allowed_roles}.")
        return value

    def validate_place(self, value):
        if value and not Place.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Place does not exist.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, validators=[phone_validator])

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "email"]
    
    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        return value.strip().capitalize()

    def validate_last_name(self, value):
        if value:
            return value.strip().capitalize()
        return value


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, validators=[phone_validator])

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "email", "is_active", "role", "place"]

    def validate_role(self, value):
        allowed_roles = [choice[0] for choice in ROLE_CHOICES]
        if value not in allowed_roles:
            raise serializers.ValidationError(f"Role must be one of {allowed_roles}.")
        return value

    def validate_place(self, value):
        if value and not Place.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Place does not exist.")
        return value
    
    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name cannot be empty.")
        return value.strip().capitalize()

    def validate_last_name(self, value):
        if value:
            return value.strip().capitalize()
        return value
