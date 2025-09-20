from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from utils.responses import success_response, error_response
from .models import HeartRateRecord
from .serializers import HeartRateRecordSerializer
from django.core.exceptions import ObjectDoesNotExist

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from apps.common.pagination import StandardResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter


class HeartRateRecordViewSet(viewsets.ModelViewSet):
    queryset = HeartRateRecord.objects.all().order_by("-recorded_at")
    serializer_class = HeartRateRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ['patient']  # filter by patient id
    ordering_fields = ['bpm', 'recorded_at']
    ordering = ['-recorded_at']

    

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by: bpm, recorded_at. Use '-' prefix for descending.",
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
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return success_response("Heart rate records retrieved successfully", serializer.data)
        except Exception as e:
            return error_response("Error retrieving heart rate records", str(e), status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            record = self.get_object()
            serializer = self.get_serializer(record)
            return success_response(
                message="Heart rate record retrieved successfully",
                data=serializer.data,
            )
        except ObjectDoesNotExist:
            return error_response(message="Heart rate record not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return error_response(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            serializer.save()
            return success_response(
                message="Heart rate recorded successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return error_response(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        serializer = self.get_serializer(record, data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            serializer.save()
            return success_response(
                message="Heart rate record updated successfully",
                data=serializer.data,
            )
        except Exception as e:
            return error_response(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        record = self.get_object()
        serializer = self.get_serializer(record, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            serializer.save()
            return success_response(
                message="Heart rate record partially updated successfully",
                data=serializer.data,
            )
        except Exception as e:
            return error_response(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            record = self.get_object()
            record.delete()
            return success_response(
                message="Heart rate record deleted successfully",
                status=status.HTTP_204_NO_CONTENT,
            )
        except ObjectDoesNotExist:
            return error_response(message="Heart rate record not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return error_response(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
