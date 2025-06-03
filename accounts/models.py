from datetime import timedelta
import uuid
import base64
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


def generate_short_uuid():
    u = uuid.uuid4()
    b64 = base64.urlsafe_b64encode(u.bytes).decode('utf-8').rstrip('=')
    return b64[:8]


class MemberTier(models.Model):
    # Use small int for tier id like 1,2,3
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.id} - {self.name}"


class CustomUserManager(BaseUserManager):

    def get_authentication_identifier(self):
        return self.email or self.phone_number

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('The Email or Phone number must be set')
        if email:
            email = self.normalize_email(email)
            extra_fields['email'] = email
        if phone_number:
            extra_fields['phone_number'] = phone_number
        user = self.model(**extra_fields)
        # Password is required for email or phone login
        if extra_fields.get('login_method') in ['email', 'phone']:
            if not password:
                raise ValueError(
                    'Password is required for email or phone login')
            user.set_password(password)
        else:
            # For social login, password may not be set
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('login_method', 'email')
        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    LOGIN_METHOD_CHOICES = [
        ('email', 'Email/Password'),
        ('phone', 'Phone/Password'),
        ('google', 'Google'),
        ('apple', 'Apple'),
    ]
    user_id = models.CharField(
        max_length=8,
        unique=True,
        editable=False,
        null=False,
        default=generate_short_uuid,  # function is now defined above
    )
    member_tier = models.ForeignKey(
        MemberTier, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(
        max_length=20, unique=True, null=True, blank=True)
    salutation = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    login_method = models.CharField(
        max_length=10, choices=LOGIN_METHOD_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.phone_number or 'User'


def default_expiry():
    return timezone.now() + timedelta(minutes=5)


class OTP(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)  # OTP valid for 5 minutes
        super().save(*args, **kwargs)
