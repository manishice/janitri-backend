from django.db import models
from django.conf import settings

# Create your models here.

class Alert(models.Model):
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="alerts")
    record = models.ForeignKey("records.HeartRateRecord", on_delete=models.CASCADE, related_name="alerts")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts_resolved"
    )

    def __str__(self):
        return f"Alert for {self.patient.name}: {self.message}"
