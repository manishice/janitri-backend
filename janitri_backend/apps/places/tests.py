from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.places.models import Place
from apps.users.models import User

class PlaceTests(APITestCase):
    def setUp(self):
        # Create Admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", first_name="Admin", last_name="User", password="adminpass"
        )
        self.client.force_authenticate(user=self.admin_user)

        # Create a Place
        self.place = Place.objects.create(
            name="Test Clinic", address="123 Street", phone="9876543210", email="clinic@test.com"
        )

    def test_create_place(self):
        url = reverse("place-list")  # Replace with your URL name
        data = {
            "name": "New Clinic",
            "address": "456 Street",
            "phone": "9876543211",
            "email": "newclinic@test.com",
            "is_active": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Place.objects.filter(name="New Clinic").exists())

    def test_create_place_invalid_phone(self):
        url = reverse("place-list")
        data = {
            "name": "Bad Clinic",
            "phone": "abcd1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_place_blank_name(self):
        url = reverse("place-list")
        data = {
            "name": "",
            "phone": "9876543212"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_place(self):
        url = reverse("place-detail", args=[self.place.id])
        data = {"name": "Updated Clinic"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.place.refresh_from_db()
        self.assertEqual(self.place.name, "Updated Clinic")

    def test_get_place_list(self):
        url = reverse("place-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("data", [])), 1)
