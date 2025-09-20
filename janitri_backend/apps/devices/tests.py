from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.places.models import Place
from apps.patients.models import Patient
from apps.devices.models import Device
from apps.users.models import User

class DeviceTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", first_name="Admin", last_name="User", password="adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)

        # Create Place and Patient
        self.place = Place.objects.create(name="Test Clinic")
        self.patient = Patient.objects.create(name="John Doe", age=30, gender="M", place=self.place)

        # Create Device
        self.device = Device.objects.create(device_id="DEV123", place=self.place, assigned_to=self.patient)

    def test_create_device(self):
        url = reverse("device-list")  # Replace with your URL name
        new_patient = Patient.objects.create(name="Jane Doe", age=28, gender="F", place=self.place)

        data = {
            "device_id": "DEV456",
            "place": self.place.id,
            "assigned_to": new_patient.id,
            "is_active": True
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Device.objects.filter(device_id="DEV456").exists())

    def test_create_device_duplicate_device_id(self):
        url = reverse("device-list")
        data = {
            "device_id": "DEV123",  # duplicate
            "place": self.place.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_device_invalid_place(self):
        url = reverse("device-list")
        data = {
            "device_id": "DEV789",
            "place": 999  # non-existent
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_device_list(self):
        url = reverse("device-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("data", [])), 1)

    def test_update_device_assign_patient(self):
        url = reverse("device-detail", args=[self.device.id])
        # Unassign patient
        data = {"assigned_to": None}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.device.refresh_from_db()
        self.assertIsNone(self.device.assigned_to)

