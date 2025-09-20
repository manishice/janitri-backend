from rest_framework import serializers
from .models import Alert
from apps.patients.serializers import PatientSerializer
from apps.records.serializers import HeartRateRecordSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class AlertSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source="patient", read_only=True)
    record_detail = HeartRateRecordSerializer(source="record", read_only=True)
    resolved_by_detail = serializers.StringRelatedField(source="resolved_by", read_only=True)

    class Meta:
        model = Alert
        fields = [
            "id",
            "patient",
            "patient_detail",
            "record",
            "record_detail",
            "message",
            "created_at",
            "resolved",
            "resolved_at",
            "resolved_by",
            "resolved_by_detail",
        ]
        read_only_fields = ["created_at", "resolved_at", "resolved_by"]
