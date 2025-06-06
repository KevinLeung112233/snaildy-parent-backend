# accounts/serializers.py

import re
from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.backends import UserModel
from .models import CustomUser
from django.contrib.auth import authenticate, get_user_model
from student.models import StudentSession

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    login_method = serializers.ChoiceField(
        choices=CustomUser.LOGIN_METHOD_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password', 'login_method',
                  'salutation', 'first_name', 'last_name')

    def validate(self, attrs):
        login_method = attrs.get('login_method')
        email = attrs.get('email')
        phone = attrs.get('phone_number')

        if login_method == 'email' and not email:
            raise serializers.ValidationError(
                "Email is required for email login")
        if login_method == 'phone' and not phone:
            raise serializers.ValidationError(
                "Phone number is required for phone login")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.is_active = False  # inactive until OTP verified
        user.set_password(password)
        user.save()
        return user


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone_number')
        otp = attrs.get('otp')

        if not email and not phone:
            raise serializers.ValidationError(
                "Email or phone number is required")
        if not otp:
            raise serializers.ValidationError("OTP is required")
        return attrs


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # email or phone
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')
        request = self.context.get('request')

        if not identifier or not password:
            raise serializers.ValidationError(
                "Must include 'identifier' and 'password'")

        # Simple regex to check if identifier is email
        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", identifier)

        # Prepare authentication parameters
        auth_kwargs = {'password': password, 'request': request}

        if is_email:
            auth_kwargs['email'] = identifier
        else:
            auth_kwargs['phone_number'] = identifier

        user = authenticate(**auth_kwargs)

        if not user:
            # Check if user exists but is inactive
            try:
                if is_email:
                    user = CustomUser.objects.get(email=identifier)
                else:
                    user = CustomUser.objects.get(phone_number=identifier)

                if not user.is_active:
                    raise serializers.ValidationError(
                        "User account not active. Please verify your account."
                    )
            except CustomUser.DoesNotExist:
                pass  # User doesn't exist at all

            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs


class StudentSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSession
        fields = ['session_id', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):

    student_sessions = StudentSessionSerializer(
        source='student_sessions', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'student_sessions']
