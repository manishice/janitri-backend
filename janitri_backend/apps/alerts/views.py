from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from utils.responses import success_response, error_response
from .models import Alert
from .serializers import AlertSerializer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.common.pagination import StandardResultsSetPagination

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by("-created_at")
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient', 'resolved', 'resolved_by']
    ordering_fields = ['created_at', 'resolved_at']
    ordering = ['-created_at']

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by any of: created_at, resolved_at. Use '-' prefix for descending.",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.paginator.get_paginated_response(serializer.data)
                return paginated_response

            serializer = self.get_serializer(queryset, many=True)
            return success_response(message="Alerts retrieved successfully", data=serializer.data)
        except Exception as e:
            return error_response("Error retrieving alerts", str(e), status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            alert = self.get_object()
            serializer = self.get_serializer(alert)
            return success_response(serializer.data)
        except Alert.DoesNotExist:
            return error_response("Alert not found", status=404)
        except Exception as e:
            return error_response("Error retrieving alert", str(e), status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            alert = serializer.save()
            return success_response(message="Alert created", data=serializer.data, status=201)
        except Exception as e:
            return error_response("Error creating alert", str(e), status=500)

    def update(self, request, *args, **kwargs):
        try:
            alert = self.get_object()
            serializer = self.get_serializer(alert, data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            serializer.save()
            return success_response(message="Alert updated", data=serializer.data)
        except Alert.DoesNotExist:
            return error_response("Alert not found", status=404)
        except Exception as e:
            return error_response("Error updating alert", str(e), status=500)

    def partial_update(self, request, *args, **kwargs):
        try:
            alert = self.get_object()
            serializer = self.get_serializer(alert, data=request.data, partial=True)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            serializer.save()
            return success_response(message="Alert partially updated", data=serializer.data)
        except Alert.DoesNotExist:
            return error_response("Alert not found", status=404)
        except Exception as e:
            return error_response("Error partially updating alert", str(e), status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            alert = self.get_object()
            alert.delete()
            return success_response(None, message="Alert deleted")
        except Alert.DoesNotExist:
            return error_response("Alert not found", status=404)
        except Exception as e:
            return error_response("Error deleting alert", str(e), status=500)

    @action(detail=True, methods=["post"], url_path="resolve")
    def resolve_alert(self, request, pk=None):
        try:
            alert = self.get_object()
            if alert.resolved:
                return error_response("Alert is already resolved")

            alert.resolved = True
            alert.resolved_at = timezone.now()
            alert.resolved_by = request.user
            alert.save()

            serializer = self.get_serializer(alert)
            return success_response(message="Alert marked as resolved", data=serializer.data)
        except Alert.DoesNotExist:
            return error_response("Alert not found", status=404)
        except Exception as e:
            return error_response("Error resolving alert", str(e), status=500)
