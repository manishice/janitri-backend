from django.db import models
from apps.common.models import BaseModel

# Create your models here.
class Place(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
