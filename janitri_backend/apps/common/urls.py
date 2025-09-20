from django.urls import path
from .views import choices_view

urlpatterns = [
    path("choices/", choices_view, name="choices"),
]
