from django.db import models
from apps.common.models import BaseModel

# Create your models here.

class Device(BaseModel):
    device_id = models.CharField(max_length=100, unique=True)
    place = models.ForeignKey("places.Place", on_delete=models.CASCADE, related_name="devices")
    assigned_to = models.OneToOneField("patients.Patient", on_delete=models.SET_NULL, null=True, blank=True, related_name="device")
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"Device {self.device_id}"
