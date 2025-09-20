from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import get_user_model
from utils.responses import success_response, error_response
from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from utils.services.email.send_mail import send_email
from utils.resource.otp.otp_handler import generate_otp, store_otp, verify_otp, delete_otp

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "login":
            return LoginSerializer
        if self.action == "logout":
            return LogoutSerializer
        if self.action == "change_password":
            return ChangePasswordSerializer
        if self.action == "forgot_password":
            return ForgotPasswordSerializer
        if self.action == "reset_password":
            return ResetPasswordSerializer
        return LoginSerializer  # fallback

    @action(detail=False, methods=["post"], url_path="login", permission_classes=[AllowAny])
    def login(self, request):
        try:
            serializer = LoginSerializer(data=request.data, context={"request": request})
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)

            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            response_data = {
                "tokens": {"access": str(refresh.access_token), "refresh": str(refresh)},
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                },
            }
            return success_response("Login successful", response_data)
        except Exception as e:
            return error_response("Error during login", str(e), status=500)

    @action(detail=False, methods=["post"], url_path="logout", permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            serializer = LogoutSerializer(data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)

            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)

            if str(token.payload.get("user_id")) != str(request.user.id):
                return error_response("Invalid token", status=400)

            token.blacklist()
            return success_response("Logout successful")
        except (TokenError, InvalidToken) as ex:
            return error_response("Refresh token is invalid or expired", str(ex), status=400)
        except Exception as e:
            return error_response("Error during logout", str(e), status=500)

    @action(detail=False, methods=["post"], url_path="change-password", permission_classes=[IsAuthenticated])
    def change_password(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)

            user = request.user
            if not user.check_password(serializer.validated_data["old_password"]):
                return error_response("Old password is incorrect", status=400)

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return success_response("Password changed successfully")
        except Exception as e:
            return error_response("Error changing password", str(e), status=500)

    @action(detail=False, methods=["post"], url_path="forgot-password", permission_classes=[AllowAny])
    def forgot_password(self, request):
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)

            email = serializer.validated_data["email"]

            try:
                user = User.objects.get(email=email)

                otp = generate_otp()
                store_otp(email, otp)

                context = {
                    "user": user,
                    "otp": otp,
                    "expiry_minutes": 5,
                }

                send_email(
                    subject="Your Password Reset OTP",
                    to_email=email,
                    template_name="password_reset",
                    context=context,
                )

                return success_response("OTP sent to your email")

            except User.DoesNotExist:
                return error_response("User not found", status=404)

        except Exception as e:
            return error_response("Error during forgot password", str(e), status=500)

    @action(detail=False, methods=["post"], url_path="reset-password", permission_classes=[AllowAny])
    def reset_password(self, request):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return error_response("Validation error", serializer.errors, status=400)

            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]
            new_password = serializer.validated_data["new_password"]

            if not verify_otp(email, otp):
                return error_response("Invalid or expired OTP", status=400)

            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                delete_otp(email)
                return success_response("Password reset successfully")
            except User.DoesNotExist:
                return error_response("User not found", status=404)

        except Exception as e:
            return error_response("Error during password reset", str(e), status=500)
