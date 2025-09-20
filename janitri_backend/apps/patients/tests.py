from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.places.models import Place
from apps.patients.models import Patient, Guardian
from apps.users.models import User

class PatientGuardianTests(APITestCase):
    def setUp(self):
        # Create Place and Admin user
        self.place = Place.objects.create(name="Test Clinic")
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", first_name="Admin", last_name="User", password="adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)

        # Create a Patient
        self.patient = Patient.objects.create(
            name="John Doe", age=35, gender="M", place=self.place
        )

    # ----------------- Patient Tests -----------------
    def test_create_patient(self):
        url = reverse("patient-list")  # Replace with your URL name
        data = {"name": "Alice", "age": 30, "gender": "F", "place": self.place.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Patient.objects.filter(name="Alice").exists())

    def test_create_patient_invalid_gender(self):
        url = reverse("patient-list")
        data = {"name": "Bob", "age": 25, "gender": "X", "place": self.place.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ----------------- Guardian Tests -----------------
    def test_create_guardian(self):
        url = reverse("patient-guardian-list")  # Replace with your URL name
        data = {
            "name": "Jane Doe",
            "phone": "9876543210",
            "relation": "Spouse",
            "patient": self.patient.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Guardian.objects.filter(name="Jane Doe").exists())

    def test_create_guardian_invalid_phone(self):
        url = reverse("patient-guardian-list")
        data = {
            "name": "Mike Doe",
            "phone": "abc123",
            "relation": "Father",
            "patient": self.patient.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_guardian_invalid_relation(self):
        url = reverse("patient-guardian-list")
        data = {
            "name": "Sara Doe",
            "phone": "9876543211",
            "relation": "Cousin",
            "patient": self.patient.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
