# apps/alerts/tasks.py

from celery import shared_task
from utils.services.email.send_mail import send_email  # import your utility

@shared_task
def send_alert_email_task(to_email, patient_name, patient_id, bpm, recorded_at):
    subject = "Critical Heart Rate Alert"
    context = {
        "patient_name": patient_name,
        "patient_id": patient_id,
        "bpm": bpm,
        "recorded_at": recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    # Use your reusable utility
    send_email(
        subject=subject,
        to_email=to_email,
        template_name="alert_email",
        context=context
    )
