from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from utils.responses import success_response, error_response
from .models import Device
from .serializers import DeviceSerializer
from apps.common.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.common.serializers import StatusUpdateSerializer
from rest_framework.decorators import action


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['place', 'is_active', 'assigned_to']
    ordering_fields = ['device_id', 'created_at', 'is_active']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by any of: device_id, is_active, created_at. Use '-' prefix for descending.",
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
            return success_response(message="Devices retrieved successfully", data=serializer.data)
        except Exception as e:
            return error_response("Error retrieving devices", str(e), status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            device = self.get_object()
            serializer = self.get_serializer(device)
            return success_response("Device retrieved successfully", serializer.data)
        except Device.DoesNotExist:
            return error_response("Device not found", status=404)
        except Exception as e:
            return error_response("Error retrieving device", str(e), status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_create(serializer)
            return success_response("Device created successfully", serializer.data, status=201)
        except Exception as e:
            return error_response("Error creating device", str(e), status=500)

    def update(self, request, *args, **kwargs):
        try:
            device = self.get_object()
            serializer = self.get_serializer(device, data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_update(serializer)
            return success_response("Device updated successfully", serializer.data)
        except Device.DoesNotExist:
            return error_response("Device not found", status=404)
        except Exception as e:
            return error_response("Error updating device", str(e), status=500)

    def partial_update(self, request, *args, **kwargs):
        try:
            device = self.get_object()
            serializer = self.get_serializer(device, data=request.data, partial=True)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_update(serializer)
            return success_response("Device partially updated successfully", serializer.data)
        except Device.DoesNotExist:
            return error_response("Device not found", status=404)
        except Exception as e:
            return error_response("Error partially updating device", str(e), status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            device = self.get_object()
            device.delete()
            return success_response("Device deleted successfully", status=204)
        except Device.DoesNotExist:
            return error_response("Device not found", status=404)
        except Exception as e:
            return error_response("Error deleting device", str(e), status=500)
        
    
    @extend_schema(
        description="Toggle device active/inactive status",
        request=None,
        responses={200: StatusUpdateSerializer},
    )
    @action(detail=True, methods=['patch'], url_path="change-status")
    def change_status(self, request, pk=None):
        try:
            device = self.get_object()
            device.is_active = not device.is_active
            device.save(update_fields=["is_active", "modified_at"])
            return success_response(
                message=f"Device status updated to {'Active' if device.is_active else 'Inactive'}",
                data={"id": device.id, "is_active": device.is_active}
            )
        except Exception as e:
            return error_response("Error changing device status", str(e), status=500)