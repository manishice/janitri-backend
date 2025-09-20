from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet

router = DefaultRouter()
router.register(r'place', PlaceViewSet, basename='place')

urlpatterns = [
    path('', include(router.urls))
]
