# Generated by Django 5.2.1 on 2025-06-06 09:56

import accounts.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberTier',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='會員等級名稱')),
            ],
            options={
                'verbose_name': '會員等級',
                'verbose_name_plural': '會員等級',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.CharField(default=accounts.models.generate_short_uuid, editable=False, max_length=8, unique=True, verbose_name='會員編號')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='電子郵件')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='電話號碼')),
                ('salutation', models.CharField(blank=True, max_length=20, null=True, verbose_name='稱謂')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='名字')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='姓氏')),
                ('login_method', models.CharField(choices=[('email', 'Email/密碼'), ('phone', '電話/密碼'), ('google', 'Google'), ('apple', 'Apple')], max_length=10, verbose_name='登入方式')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否啟用')),
                ('is_staff', models.BooleanField(default=False, verbose_name='是否管理員')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('member_tier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.membertier', verbose_name='會員等級')),
            ],
            options={
                'verbose_name': '會員',
                'verbose_name_plural': '會員',
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6, verbose_name='驗證碼')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('expires_at', models.DateTimeField(default=accounts.models.default_expiry, verbose_name='過期時間')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='會員')),
            ],
            options={
                'verbose_name': '一次性密碼',
                'verbose_name_plural': '一次性密碼',
            },
        ),
    ]
