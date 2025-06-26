from accounts.models import CustomUser
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from accounts.models import MemberTier
from accounts.utils import verify_apple_identity_token, verify_google_token
from .serializers import RegisterSerializer, OTPVerifySerializer, LoginSerializer, UserIdentifierCheckSerializer, UserProfileSerializer
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


class CheckUserExistView(APIView):
    def post(self, request):
        serializer = UserIdentifierCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data['identifier']

        # Simple heuristic: check if identifier looks like email
        if '@' in identifier:
            filter_kwargs = {'email': identifier}
        else:
            filter_kwargs = {'phone_number': identifier}

        try:
            user = User.objects.get(**filter_kwargs)
        except User.DoesNotExist:
            return Response({
                "exists": False,
                "is_active": False,
                "message": "User not found."
            }, status=status.HTTP_200_OK)

        return Response({
            "exists": True,
            "is_active": user.is_active,
            "message": "User found."
        }, status=status.HTTP_200_OK)


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
            return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
        else:
            # FIXME: Implement SMS OTP sending for phone
            return Response({
                "message": "OTP generated for phone",
                "otp": otp_code  # Remove in production! Only for development
            }, status=status.HTTP_200_OK)


class TokenRefreshView(generics.GenericAPIView):
    def post(self, request):
        print("refresh_token_str", request.data)

        refresh_token_str = request.data.get('refresh-token')
        print("refresh_token_str", refresh_token_str)
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


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({"detail": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        idinfo = verify_google_token(token)
        if not idinfo:
            return Response({"detail": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

        email = idinfo.get('email')
        if not email:
            return Response({"detail": "Email not available in token"}, status=status.HTTP_400_BAD_REQUEST)

        google_sub = idinfo.get('sub')
        user, created = User.objects.get_or_create(
            google_id=google_sub,
            defaults={
                'email': idinfo.get('email'),
                'login_method': 'google',
                'is_active': True,
                'first_name': idinfo.get('given_name', ''),
                'last_name': idinfo.get('family_name', ''),
                # Set other defaults as needed
            }
        )

        # If user exists but login_method is not google, you may want to handle that case

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class AppleLoginView(APIView):
    def post(self, request):
        identity_token = request.data.get('token')
        authorization_code = request.data.get(
            'authorization_code')  # Optional, for further validation

        if not identity_token:
            return Response({"detail": "identity_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify Apple identity token
        payload = verify_apple_identity_token(
            identity_token, audience='com.snaildy.snaildyParentApp')
        if not payload:
            return Response({"detail": "Invalid Apple identity token"}, status=status.HTTP_400_BAD_REQUEST)

        email = payload.get('email')
        apple_sub = payload.get('sub')  # unique Apple user ID

        if not email or not apple_sub:
            return Response({"detail": "Email or sub missing in token"}, status=status.HTTP_400_BAD_REQUEST)

        apple_sub = payload.get('sub')
        # Lookup or create user
        user, created = User.objects.get_or_create(
            apple_id=apple_sub,
            defaults={
                'email': payload.get('email'),
                'login_method': 'apple',
                'is_active': True,
                'first_name': request.data.get('given_name') or '',
                'last_name': request.data.get('family_name') or '',
            }
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
