# records/signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import HeartRateRecord
from apps.alerts.models import Alert
from apps.alerts.tasks import send_alert_email_task  # Celery task
from apps.users.models import User  # Doctor model

logger = logging.getLogger(__name__)

CRITICAL_HIGH = getattr(settings, "ALERT_CRITICAL_HIGH", 120)
CRITICAL_LOW = getattr(settings, "ALERT_CRITICAL_LOW", 40)


@receiver(post_save, sender=HeartRateRecord)
def create_critical_alert(sender, instance, created, **kwargs):
    """
    Create an Alert when a HeartRateRecord is critical.
    Send email to doctors asynchronously via Celery.
    """
    print("hoo")
    if not created:
        return

    bpm = instance.bpm
    patient = instance.patient

    if bpm > CRITICAL_HIGH:
        message = f"Critical high heart rate detected: {bpm} bpm"
    elif bpm < CRITICAL_LOW:
        message = f"Critical low heart rate detected: {bpm} bpm"
    else:
        # Not critical, nothing to do
        logger.debug("HeartRateRecord not critical: %s bpm (patient=%s)", bpm, patient)
        return

    # Create Alert (OneToOne ensures no duplicates)
    alert, created_alert = Alert.objects.get_or_create(
        record=instance,
        defaults={"patient": patient, "message": message},
    )

    if created_alert:
        logger.info("Created Alert(id=%s) for HeartRateRecord(id=%s)", alert.id, instance.id)

        # Notify all doctors in the same place
        doctors = User.objects.filter(place=patient.place, role="DOCTOR")
        for doctor in doctors:
            if doctor.email:
                # Call Celery task to send email
                send_alert_email_task.delay(
                    to_email=doctor.email,
                    patient_name=patient.name,
                    patient_id=patient.id,
                    bpm=bpm,
                    recorded_at=instance.recorded_at
                )
    else:
        logger.debug("Alert already exists for HeartRateRecord(id=%s)", instance.id)
