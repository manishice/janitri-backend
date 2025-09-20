from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from utils.constants.choices import ROLE_CHOICES

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("role") != "ADMIN":
            raise ValueError("Superuser must have role=ADMIN.")

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None  # disable default username
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="DOCTOR")
    place = models.ForeignKey("places.Place", on_delete=models.SET_NULL, null=True, blank=True, related_name="staff")
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
