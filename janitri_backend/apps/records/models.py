from django.db import models

# Create your models here.

class HeartRateRecord(models.Model):
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="heart_records")
    bpm = models.PositiveIntegerField(help_text="Beats per minute")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.bpm} bpm"
