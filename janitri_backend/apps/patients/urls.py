from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, GuardianViewSet

router = DefaultRouter()
router.register(r'patient', PatientViewSet, basename='patient')
router.register(r'patient-guardian', GuardianViewSet, basename='patient-guardian') 

urlpatterns = [
    path('', include(router.urls))
]
