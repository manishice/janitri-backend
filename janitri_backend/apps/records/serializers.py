from rest_framework import serializers
from .models import HeartRateRecord
from apps.patients.serializers import PatientSerializer

class HeartRateRecordSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source="patient", read_only=True)

    class Meta:
        model = HeartRateRecord
        fields = ["id", "patient", "patient_detail", "bpm", "recorded_at"]
        read_only_fields = ["recorded_at"]
