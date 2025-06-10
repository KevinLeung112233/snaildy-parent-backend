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
    id = models.PositiveSmallIntegerField(
        primary_key=True, verbose_name="id")
    name = models.CharField(max_length=50, unique=True, verbose_name="會員等級名稱")

    class Meta:
        verbose_name = "會員等級"
        verbose_name_plural = "會員等級"

    def __str__(self):
        return f"{self.id} - {self.name}"


class CustomUserManager(BaseUserManager):

    def get_authentication_identifier(self):
        return self.email or self.phone_number

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('必須提供 Email 或電話號碼')
        if email:
            email = self.normalize_email(email)
            extra_fields['email'] = email
        if phone_number:
            extra_fields['phone_number'] = phone_number
        user = self.model(**extra_fields)
        if extra_fields.get('login_method') in ['email', 'phone']:
            if not password:
                raise ValueError('使用 Email 或電話登入必須設定密碼')
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('login_method', 'email')
        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email  # fallback to email or username

    def get_short_name(self):
        return self.first_name or self.email

    LOGIN_METHOD_CHOICES = [
        ('email', 'Email/密碼'),
        ('phone', '電話/密碼'),
        ('google', 'Google'),
        ('apple', 'Apple'),
    ]
    user_id = models.CharField(
        max_length=8,
        unique=True,
        editable=False,
        null=False,
        default=generate_short_uuid,
        verbose_name="會員編號"
    )
    member_tier = models.ForeignKey(
        MemberTier, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="會員等級")
    email = models.EmailField(unique=True, null=True,
                              blank=True, verbose_name="電子郵件")
    phone_number = models.CharField(
        max_length=20, unique=True, null=True, blank=True, verbose_name="電話號碼")
    salutation = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="稱謂")
    first_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="名字")
    last_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="姓氏")
    login_method = models.CharField(
        max_length=10, choices=LOGIN_METHOD_CHOICES, verbose_name="登入方式")
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name="加入日期")

    is_active = models.BooleanField(default=True, verbose_name="Activated")
    is_staff = models.BooleanField(default=False, verbose_name="是否管理員")
    is_mentor = models.BooleanField(default=False, verbose_name="是否導師")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "會員"
        verbose_name_plural = "會員"

    def __str__(self):
        return self.email or self.phone_number or '會員'


def default_expiry():
    return timezone.now() + timedelta(minutes=5)


class OTP(models.Model):
    user = models.ForeignKey('accounts.CustomUser',
                             on_delete=models.CASCADE, verbose_name="會員")
    code = models.CharField(max_length=6, verbose_name="驗證碼")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    expires_at = models.DateTimeField(
        default=default_expiry, verbose_name="過期時間")

    class Meta:
        verbose_name = "一次性密碼"
        verbose_name_plural = "一次性密碼"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)  # OTP valid for 5 minutes
        super().save(*args, **kwargs)
