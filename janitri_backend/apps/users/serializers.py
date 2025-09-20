from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.utils.crypto import get_random_string

User = get_user_model()


# ---------- BASE SERIALIZERS ----------
class UserSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "phone", "address"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AdminCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "address", "role", "place"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # TODO: send email with temp_password
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Update profile for self."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "email"]


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """Update profile for admin."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "email", "is_active", "role", "place"]

