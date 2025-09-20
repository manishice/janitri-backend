from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from utils.responses import success_response, error_response
from .models import Patient, Guardian
from .serializers import PatientSerializer, GuardianSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from apps.common.pagination import StandardResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['place', 'age', 'gender']
    ordering_fields = ['age', 'created_at', 'name']  # allowed ordering via query params
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)
        
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='ordering',
                description='Order by any of: name, age, created_at. Use "-" prefix for descending.',
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

            # If pagination not applied
            serializer = self.get_serializer(queryset, many=True)
            return success_response(message="Patients retrieved successfully", data=serializer.data)
        except Exception as e:
            return error_response(message="Error retrieving patients", errors=str(e), status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            patient = self.get_object()
            serializer = self.get_serializer(patient)
            return success_response("Patient retrieved successfully", serializer.data)
        except Patient.DoesNotExist:
            return error_response("Patient not found", status=404)
        except Exception as e:
            return error_response("Error retrieving patient", str(e), status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_create(serializer)
            return success_response("Patient created successfully", serializer.data, status=201)
        except Exception as e:
            return error_response("Error creating patient", str(e), status=500)

    def update(self, request, *args, **kwargs):
        try:
            patient = self.get_object()
            serializer = self.get_serializer(patient, data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_update(serializer)
            return success_response("Patient updated successfully", serializer.data)
        except Patient.DoesNotExist:
            return error_response("Patient not found", status=404)
        except Exception as e:
            return error_response("Error updating patient", str(e), status=500)

    def partial_update(self, request, *args, **kwargs):
        try:
            patient = self.get_object()
            serializer = self.get_serializer(patient, data=request.data, partial=True)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_update(serializer)
            return success_response("Patient partially updated successfully", serializer.data)
        except Patient.DoesNotExist:
            return error_response("Patient not found", status=404)
        except Exception as e:
            return error_response("Error partially updating patient", str(e), status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            patient = self.get_object()
            patient.delete()
            return success_response("Patient deleted successfully", status=204)
        except Patient.DoesNotExist:
            return error_response("Patient not found", status=404)
        except Exception as e:
            return error_response("Error deleting patient", str(e), status=500)


class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient', 'relation', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by any of: name, created_at. Use '-' prefix for descending.",
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
            return success_response(message="Guardians retrieved successfully", data=serializer.data)
        except Exception as e:
            return error_response("Error retrieving guardians", str(e), status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            guardian = self.get_object()
            serializer = self.get_serializer(guardian)
            return success_response("Guardian retrieved successfully", serializer.data)
        except Guardian.DoesNotExist:
            return error_response("Guardian not found", status=404)
        except Exception as e:
            return error_response("Error retrieving guardian", str(e), status=500)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_create(serializer)
            return success_response("Guardian created successfully", serializer.data, status=201)
        except Exception as e:
            return error_response("Error creating guardian", str(e), status=500)

    def update(self, request, *args, **kwargs):
        try:
            guardian = self.get_object()
            serializer = self.get_serializer(guardian, data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_update(serializer)
            return success_response("Guardian updated successfully", serializer.data)
        except Guardian.DoesNotExist:
            return error_response("Guardian not found", status=404)
        except Exception as e:
            return error_response("Error updating guardian", str(e), status=500)

    def partial_update(self, request, *args, **kwargs):
        try:
            guardian = self.get_object()
            serializer = self.get_serializer(guardian, data=request.data, partial=True)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)
            self.perform_update(serializer)
            return success_response("Guardian partially updated successfully", serializer.data)
        except Guardian.DoesNotExist:
            return error_response("Guardian not found", status=404)
        except Exception as e:
            return error_response("Error partially updating guardian", str(e), status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            guardian = self.get_object()
            guardian.delete()
            return success_response("Guardian deleted successfully", status=204)
        except Guardian.DoesNotExist:
            return error_response("Guardian not found", status=404)
        except Exception as e:
            return error_response("Error deleting guardian", str(e), status=500)
