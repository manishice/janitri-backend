from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.places.models import Place

class UserTests(APITestCase):
    def setUp(self):
        # Create a Place
        self.place = Place.objects.create(name="Test Clinic")

        # Create Admin and Doctor
        self.admin_user = User.objects.create_superuser(
            email="admin@test.com", first_name="Admin", last_name="User", password="adminpass"
        )
        self.doctor_user = User.objects.create_user(
            email="doctor@test.com", first_name="Doctor", last_name="User", password="doctorpass",
            role="DOCTOR", place=self.place
        )

        self.client.force_authenticate(user=self.admin_user)

    def test_user_registration(self):
        url = reverse("users-register")  # Replace with your actual URL name
        data = {
            "email": "newuser@test.com",
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User",
            "phone": "9876543210",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@test.com").exists())

    def test_user_registration_invalid_phone(self):
        url = reverse("users-register")
        data = {
            "email": "badphone@test.com",
            "password": "newpass123",
            "first_name": "Bad",
            "last_name": "Phone",
            "phone": "1234abc",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_create_user_invalid_role(self):
        url = reverse("users-create-user")  # Replace with your URL name
        data = {
            "email": "invalidrole@test.com",
            "first_name": "Invalid",
            "last_name": "Role",
            "role": "INVALID",
            "place": self.place.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_create_user_success(self):
        url = reverse("users-create-user")
        data = {
            "email": "doctor2@test.com",
            "first_name": "Doctor",
            "last_name": "Two",
            "role": "DOCTOR",
            "place": self.place.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="doctor2@test.com").exists())
