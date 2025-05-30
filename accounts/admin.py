from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, StudentSession, OTP, MemberTier
from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'login_method')


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'login_method',
                  'is_active', 'is_staff', 'is_superuser')


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('user_id', 'email', 'phone_number',
                    'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('user_id', 'email', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password', 'login_method')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',
         'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'login_method', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(StudentSession)
class StudentSessionAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'session_id')
    list_display = ('get_user_id', 'session_id')

    def get_user_id(self, obj):
        return obj.user.user_id
    get_user_id.short_description = 'User ID'


@admin.register(MemberTier)
class MemberTierAdmin(admin.ModelAdmin):
    # List the fields you want to display in the admin list view
    list_display = ('id', 'name')
