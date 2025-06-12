from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.apps import apps

from .models import CustomUser, MemberTier
from .forms import CustomUserCreationForm, CustomUserChangeForm
from student.models import Student  # Replace 'student' with your actual app name
from django.contrib.admin import SimpleListFilter


class HasChildFilter(SimpleListFilter):
    title = 'Has Child'
    parameter_name = 'has_child'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(students__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(students__isnull=True)
        return queryset


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0  # No empty forms by default
    readonly_fields = ('chinese_name', 'english_name',
                       'grade', 'school')  # Customize as needed
    can_delete = False  # Optional: prevent deletion through parent admin
    show_change_link = True  # Add link to individual student admin

    def has_add_permission(self, request, obj=None):
        return False  # Optional: disable adding new students here


class CustomUserAdmin(BaseUserAdmin):

    # Use the form with password1 and password2 here
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ('user_id',)
    inlines = [StudentInline]

    list_display = ('user_id', 'first_name', 'last_name', 'email', 'phone_number', 'date_joined', 'is_active',
                    'is_staff', 'is_mentor', 'has_child')
    list_filter = ('is_staff', 'is_mentor', 'first_name',
                   'last_name', 'is_superuser', 'is_active', HasChildFilter)
    search_fields = ('user_id', 'email', 'first_name',
                     'last_name', 'phone_number',)
    ordering = ('email', 'first_name', 'last_name', 'date_joined', 'is_active')

    @admin.display(boolean=True, description='Has Child')
    def has_child(self, obj):
        return obj.students.exists()

    fieldsets = (
        (None, {'fields': ('user_id', 'first_name', 'last_name', 'email',
         'phone_number', 'password', 'login_method')}),
        ('Permissions', {'fields': ('is_staff', 'is_mentor', 'is_superuser',
                                    'is_active',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'login_method', 'password1', 'password2', 'is_staff', 'is_mentor', 'is_superuser', 'is_active')}
         ),
    )


CustomUser._meta.verbose_name = "會員"
CustomUser._meta.verbose_name_plural = "會員"

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(MemberTier)
class MemberTierAdmin(admin.ModelAdmin):
    # List the fields you want to display in the admin list view
    list_display = ('id', 'name')


HIDE_MODELS = [
    ('account', 'EmailAddress'),  # django-allauth email addresses
    ('auth', 'Group'),
    ('socialaccount', 'SocialAccount'),
    ('socialaccount', 'SocialApp'),
    ('socialaccount', 'SocialToken'),
]

for app_label, model_name in HIDE_MODELS:
    try:
        model = apps.get_model(app_label, model_name)
        admin.site.unregister(model)
    except (admin.sites.NotRegistered, LookupError) as e:
        pass
