from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from utils.responses import success_response, error_response
from .models import Place
from .serializers import PlaceSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from apps.common.pagination import StandardResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from apps.common.serializers import StatusUpdateSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ['name', 'is_active']
    ordering_fields = ['name', 'created_at', 'modified_at']
    ordering = ['-created_at']


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Order by: name, created_at, modified_at. Use '-' prefix for descending.",
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
            return success_response("Places retrieved successfully", serializer.data)
        except Exception as e:
            return error_response("Error retrieving places", str(e), status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            place = self.get_object()
            serializer = self.get_serializer(place)
            return success_response(
                message="Place retrieved successfully",
                data=serializer.data,
            )
        except Place.DoesNotExist:
            return error_response("Place not found", status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_create(serializer)
        return success_response(
            message="Place created successfully",
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        place = self.get_object()
        serializer = self.get_serializer(place, data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_update(serializer)
        return success_response(
            message="Place updated successfully",
            data=serializer.data,
        )

    def partial_update(self, request, *args, **kwargs):
        place = self.get_object()
        serializer = self.get_serializer(place, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(
                message=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_update(serializer)
        return success_response(
            message="Place partially updated successfully",
            data=serializer.data,
        )

    def destroy(self, request, *args, **kwargs):
        try:
            place = self.get_object()
            place.is_active = False
            place.modified_by = request.user  # ensure modified_by is updated
            place.save(update_fields=["is_active", "modified_by"])
            return success_response(
                message="Place deactivated successfully",
                status=status.HTTP_204_NO_CONTENT,
            )
        except Place.DoesNotExist:
            return error_response("Place not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return error_response(message=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(
        description="Toggle place active/inactive status",
        request=None,
        responses={200: StatusUpdateSerializer},
    )
    @action(detail=True, methods=['patch'], url_path="change-status")
    def change_status(self, request, pk=None):
        try:
            place = self.get_object()
            place.is_active = not place.is_active
            place.save(update_fields=["is_active", "modified_at"])
            return success_response(
                message=f"Place status updated to {'Active' if place.is_active else 'Inactive'}",
                data={"id": place.id, "is_active": place.is_active}
            )
        except Exception as e:
            return error_response("Error changing place status", str(e), status=500)

