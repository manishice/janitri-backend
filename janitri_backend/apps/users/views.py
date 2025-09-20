# apps/users/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.db import DatabaseError

from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    AdminCreateUserSerializer,
    UserUpdateSerializer,
    AdminUserUpdateSerializer,
)
from apps.common.serializers import StatusUpdateSerializer
from .permissions import IsAdminRole, IsSelfOrAdmin
from utils.responses import success_response, error_response
from utils.services.email.send_mail import send_email

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from apps.common.pagination import StandardResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    User management API:
    - Default actions: list, retrieve, create, update, partial_update, destroy
    - Custom actions: register, me, update_profile, create_user, change_status
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    # Allow filtering on key fields
    filterset_fields = ['email', 'role', 'place']
    
    # Allow ordering on these fields
    ordering_fields = ['first_name', 'last_name', 'created_at', 'modified_at']
    ordering = ['-created_at']  # default order

    def get_permissions(self):
        if self.action in ["register"]:
            return [AllowAny()]
        if self.action in ["create_user", "change_status", "list"]:
            return [IsAuthenticated(), IsAdminRole()]
        if self.action in ["update", "partial_update", "retrieve", "destroy"]:
            return [IsAuthenticated(), IsSelfOrAdmin()]
        if self.action in ["me", "update_profile"]:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "register":
            return UserRegisterSerializer
        if self.action == "create_user":
            return AdminCreateUserSerializer
        if self.action == "update_profile":
            return UserUpdateSerializer
        if self.action in ["update", "partial_update"]:
            return AdminUserUpdateSerializer
        if self.action == "change_status":
            return StatusUpdateSerializer
        return UserSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description=(
                    "Order by any of: first_name, last_name, created_at, modified_at. "
                    "Use '-' prefix for descending."
                ),
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
            return success_response(message="Users retrieved successfully", data=serializer.data)
        except Exception as e:
            return error_response("Error retrieving users", str(e), status=500)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response(message="User details retrieved", data=serializer.data)
        except User.DoesNotExist:
            return error_response(message="User not found", status=404)
        except Exception as e:
            return error_response(message="Error retrieving user", errors=str(e), status=500)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, "role", None) != "ADMIN":
            return error_response(message="Only admin can create users", status=403)
        serializer = AdminCreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message="Invalid input", errors=serializer.errors, status=400)

        try:
            user = serializer.save()
            password = get_random_string(8)
            user.set_password(password)
            user.save()

            send_email(
                subject="Welcome to Janitri - Your Account Details",
                to_email=user.email,
                template_name="welcome_email_with_credentials",
                context={"user": user, "company_name": "Janitri", "email": user.email, "password": password},
            )
            return success_response(message="User created", data=UserSerializer(user).data, status=201)
        except Exception as e:
            return error_response(message="Error creating user", errors=str(e), status=500)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            return error_response(message="Invalid input", errors=serializer.errors, status=400)

        try:
            serializer.save()
            return success_response(message="User updated", data=serializer.data)
        except Exception as e:
            return error_response(message="Error updating user", errors=str(e), status=500)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message="Invalid input", errors=serializer.errors, status=400)

        try:
            serializer.save()
            return success_response(message="User partially updated", data=serializer.data)
        except Exception as e:
            return error_response(message="Error updating user", errors=str(e), status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False  # soft delete
            instance.save()
            return success_response(message="User deactivated", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return error_response(message="Error deactivating user", errors=str(e), status=500)

    # ---------------- CUSTOM ACTIONS ----------------
    @action(detail=False, methods=["post"], url_path="register", permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message="Invalid input", errors=serializer.errors, status=400)

        try:
            user = serializer.save()
            send_email(
                subject="Welcome to Janitri",
                to_email=user.email,
                template_name="welcome_email",
                context={"user": user, "company_name": "Janitri"},
            )
            return success_response(message="Registered successfully", data=UserSerializer(user).data, status=201)
        except Exception as e:
            return error_response(message="Error during registration", errors=str(e), status=500)

    @action(detail=False, methods=["get"], url_path="me", permission_classes=[IsAuthenticated])
    def me(self, request):
        return success_response(data=UserSerializer(request.user).data)

    @action(detail=False, methods=["patch"], url_path="me/update", permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message="Invalid input", errors=serializer.errors, status=400)

        try:
            serializer.save()
            return success_response(message="Profile updated", data=serializer.data)
        except Exception as e:
            return error_response(message="Error updating profile", errors=str(e), status=500)

    @action(detail=False, methods=["post"], url_path="create-user", permission_classes=[IsAuthenticated, IsAdminRole])
    def create_user(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message="Invalid input", errors=serializer.errors, status=400)

        try:
            user = serializer.save()
            password = get_random_string(8)
            user.set_password(password)
            user.save()

            send_email(
                subject="Welcome to Janitri - Your Account Details",
                to_email=user.email,
                template_name="welcome_email_with_credentials",
                context={"user": user, "company_name": "Janitri", "email": user.email, "password": password},
            )
            return success_response(message="User created", data=UserSerializer(user).data, status=201)
        except Exception as e:
            return error_response(message="Error creating user", errors=str(e), status=500)

    @action(detail=True, methods=["patch"], url_path="change-status", permission_classes=[IsAuthenticated, IsAdminRole])
    def change_status(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message="Invalid input", errors=serializer.errors, status=400)

        try:
            user = self.get_object()
            user.is_active = serializer.validated_data["is_active"]
            user.save(update_fields=["is_active"])
            return success_response(message="User status updated", data={"id": user.id, "is_active": user.is_active})
        except Exception as e:
            return error_response(message="Internal Server Error", errors=str(e), status=500)
