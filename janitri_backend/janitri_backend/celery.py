# janitri_backend/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "janitri_backend.settings")

app = Celery("janitri_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Optional: for debugging
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
