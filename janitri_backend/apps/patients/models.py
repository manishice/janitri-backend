from django.db import models
from apps.common.models import BaseModel
from utils.constants.choices import GENDER_CHOICES, RELATION_CHOICES
# Create your models here.

class Patient(BaseModel):
    place = models.ForeignKey("places.Place", on_delete=models.CASCADE, related_name="patients")
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name


class Guardian(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="guardians")
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relation})"
