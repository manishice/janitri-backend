from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HeartRateRecordViewSet

router = DefaultRouter()
router.register(r'heart-rate-record', HeartRateRecordViewSet, basename='heart-rate-record')

urlpatterns = [
    path('', include(router.urls))
]
