from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.patients.models import Patient
from apps.records.models import HeartRateRecord
from apps.users.models import User
from apps.places.models import Place

class HeartRateRecordTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", first_name="Admin", last_name="User", password="adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)

        # Create Place and Patient
        self.place = Place.objects.create(name="Test Clinic")
        self.patient = Patient.objects.create(name="John Doe", age=30, gender="M", place=self.place)

        # Create a heart rate record
        self.record = HeartRateRecord.objects.create(patient=self.patient, bpm=75)

    def test_create_heart_rate_record(self):
        url = reverse("heart-rate-record-list")  # Replace with your URL name
        data = {"patient": self.patient.id, "bpm": 85}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(HeartRateRecord.objects.filter(patient=self.patient, bpm=85).exists())

    def test_create_heart_rate_record_invalid_bpm(self):
        url = reverse("heart-rate-record-list")
        data = {"patient": self.patient.id, "bpm": -5}  # invalid BPM
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_heart_rate_record_list(self):
        url = reverse("heart-rate-record-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("data", [])), 1)

    def test_update_heart_rate_record(self):
        url = reverse("heart-rate-record-detail", args=[self.record.id])
        data = {"bpm": 90}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(self.record.bpm, 90)
