from django.test import TestCase

# Create your tests here.
from apps.patients.models import Patient
from apps.records.models import HeartRateRecord
from apps.alerts.models import Alert
from apps.places.models import Place

class AlertSignalTests(TestCase):
    
    

    def make_patient(self):
        place = Place.objects.create(name="Test Place")  # or get an existing place
        # adjust fields to match your Patient model
        return Patient.objects.create(name="Test Patient", age=30, gender="M", place=place)

    def test_critical_high_creates_alert(self):
        p = self.make_patient()
        rec = HeartRateRecord.objects.create(patient=p, bpm=130)
        self.assertTrue(Alert.objects.filter(record=rec).exists())
        alert = Alert.objects.get(record=rec)
        self.assertIn("Critical high", alert.message)

    def test_non_critical_does_not_create_alert(self):
        p = self.make_patient()
        rec = HeartRateRecord.objects.create(patient=p, bpm=80)
        self.assertFalse(Alert.objects.filter(record=rec).exists())

    def test_critical_low_creates_alert(self):
        p = self.make_patient()
        rec = HeartRateRecord.objects.create(patient=p, bpm=30)
        self.assertTrue(Alert.objects.filter(record=rec).exists())
        alert = Alert.objects.get(record=rec)
        self.assertIn("Critical low", alert.message)

