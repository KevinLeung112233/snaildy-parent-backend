from accounts.models import CustomUser
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from accounts.models import MemberTier
from .serializers import RegisterSerializer, OTPVerifySerializer, LoginSerializer, UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.core.cache import cache
import random
from rest_framework.permissions import IsAuthenticated
from typing import Tuple
from django.utils.timezone import now


User = get_user_model()


def send_otp_email(user, otp):
    """
    Send OTP code to user's email.
    """
    print(f"Sending OTP {otp} to email: {user.email}")

    send_mail(
        subject='Your OTP Code',
        message=f'Your OTP code is {otp}',
        from_email=None,  # uses DEFAULT_FROM_EMAIL from settings.py
        recipient_list=[user.email],
        fail_silently=False,
    )


def generate_and_cache_otp(user_identifier):
    """
    Generate a 6-digit OTP, cache it for 5 minutes keyed by user identifier.
    """
    otp_code = f"{random.randint(100000, 999999)}"
    cache_key = f"otp_{user_identifier}"
    cache_timeout = 5 * 60  # 5 minutes in seconds

    # Store OTP in cache with timeout
    cache.set(cache_key, otp_code, timeout=cache_timeout)

    return otp_code


def verify_cached_otp(user: CustomUser, otp_input: str) -> Tuple[bool, str]:
    """
    Verify OTP by comparing input with cached OTP.
    On success, activate user and assign member tier id=1.
    """
    cache_key = f"otp_{user.email}"  # Use user.email as cache key
    cached_otp = cache.get(cache_key)

    if cached_otp is None:
        return False, "OTP expired or not found"

    if otp_input == cached_otp:
        cache.delete(cache_key)

        user.is_active = True

        try:
            default_tier = MemberTier.objects.get(id=1)
        except MemberTier.DoesNotExist:
            default_tier = None

        user.member_tier = default_tier
        user.save(update_fields=['is_active', 'member_tier'])

        return True, "OTP verified and user activated"

    return False, "Invalid OTP"


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        otp_type = 'email' if user.login_method == 'email' else 'phone'

        if otp_type == 'email':
            otp_code = generate_and_cache_otp(user.email)
            send_otp_email(user, otp_code)
        else:
            # FIXME: Implement SMS OTP sending for phone
            otp_code = generate_and_cache_otp(user.phone_number)
            # send_otp_sms(user.phone_number, otp_code)


class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        phone = serializer.validated_data.get('phone_number')
        otp_input = serializer.validated_data.get('otp')

        try:
            if email:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Pass user object directly to verify_cached_otp
        is_valid, message = verify_cached_otp(user, otp_input)
        if not is_valid:
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

        # At this point, user.is_active and member_tier are already updated in verify_cached_otp
        # So no need to save again here

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        user.last_login = now()
        user.save(update_fields=['last_login'])

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


# UPDATED RESEND OTP VIEW WITH BETTER ERROR HANDLING
class ResendOTPView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone_number')
        identifier = email or phone  # For better error messages

        if not identifier:
            return Response({"error": "Email or phone_number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if email:
                user = User.objects.get(email=email)
                user_identifier = user.email
                otp_type = 'email'
            else:
                user = User.objects.get(phone_number=phone)
                user_identifier = user.phone_number
                otp_type = 'phone'
        except User.DoesNotExist:
            return Response({"error": f"User with identifier '{identifier}' not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({"message": "User already verified. You can login directly."}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = generate_and_cache_otp(user_identifier)

        if otp_type == 'email':
            send_otp_email(user, otp_code)
            return Response({"message": "OTP resent to your email"}, status=status.HTTP_200_OK)
        else:
            # FIXME: Implement SMS OTP sending for phone
            return Response({
                "message": "OTP generated for phone",
                "otp": otp_code  # Remove in production! Only for development
            }, status=status.HTTP_200_OK)


# UPDATED TOKEN REFRESH VIEW
class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token_str = request.data.get('refresh_token')

        if not refresh_token_str:
            return Response({"detail": "refresh_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token_str)
            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)
            return Response({
                "access": new_access_token,
                "refresh": new_refresh_token,
            })
        except Exception as e:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
