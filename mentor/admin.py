import random
import string
from django import forms
from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Mentor
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.template.response import TemplateResponse
from django.conf import settings
from django.core.mail import send_mail
from .forms import MentorPasswordResetForm

User = get_user_model()

# Utility function for password generation


def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


# Custom form for Mentor admin including user fields as regular form fields
class MentorAdminForm(forms.ModelForm):
    first_name = forms.CharField(required=True, max_length=150)
    last_name = forms.CharField(required=True, max_length=150)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    login_method = forms.ChoiceField(
        choices=[('email', 'Email'), ('phone', 'Phone')], required=True)

    class Meta:
        model = Mentor
        fields = []  # No Mentor model fields shown

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone_number'].initial = getattr(
                user, 'phone_number', '')
            self.fields['login_method'].initial = getattr(
                user, 'login_method', '')


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    form = MentorAdminForm
    search_fields = ['user__email', 'user__username']

    def save_model(self, request, obj, form, change):
        if not change:
            # Extract user data from form.cleaned_data
            user_data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'phone_number': form.cleaned_data['phone_number'],
                'login_method': form.cleaned_data['login_method'],
            }

            # Create user instance with first_name and last_name
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                phone_number=user_data['phone_number'],
                login_method=user_data['login_method'],
                is_active=True,
                is_mentor=True,
                is_staff=True
            )
            random_password = generate_random_password()
            user.set_password(random_password)
            user.save()

            # Assign Mentor group
            mentor_group, _ = Group.objects.get_or_create(name='Mentors')
            user.groups.add(mentor_group)

            # Link user to mentor and save Mentor
            obj.user = user
            obj.save()

            if not settings.DEBUG:
                # In production: send email
                send_mail(
                    subject="您的導師帳號已建立",
                    message=(
                        f"您好，您的導師帳號已建立。\n"
                        f"帳號：{user.email}\n"
                        f"密碼：{random_password}\n"
                        "請盡快登入並更改密碼。"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            else:
                # In development: print email content to console
                print("=== Email content ===")
                print(f"To: {user.email}")
                print("Subject: 您的導師帳號已建立")
                print("Message:")
                print(
                    f"您好，您的導師帳號已建立。\n"
                    f"帳號：{user.email}\n"
                    f"密碼：{random_password}\n"
                    "請盡快登入並更改密碼。"
                )
                print("====================")
        else:
            super().save_model(request, obj, form, change)

    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path(
    #             '<path:object_id>/reset_password/',
    #             self.admin_site.admin_view(self.reset_password_view),
    #             name='mentor-reset-password',
    #         ),
    #     ]
    #     return custom_urls + urls

    # def reset_password_view(self, request, object_id):
    #     mentor = self.get_object(request, object_id)
    #     if not mentor or not mentor.user:
    #         self.message_user(
    #             request, "Mentor or linked user not found.", level=messages.ERROR)
    #         return redirect(f'../../{object_id}/change/')

    #     if request.method == 'POST':
    #         form = MentorPasswordResetForm(request.POST)
    #         if form.is_valid():
    #             new_password = form.cleaned_data['password1']
    #             user = mentor.user
    #             user.set_password(new_password)
    #             user.save()

    #             # Optionally send email notification
    #             if user.email:
    #                 send_mail(
    #                     subject="您的密碼已被重設",
    #                     message=(
    #                         f"您好，您的密碼已被管理員重設。\n"
    #                         f"新密碼：{new_password}\n"
    #                         "請盡快登入並更改密碼。"
    #                     ),
    #                     from_email=settings.DEFAULT_FROM_EMAIL,
    #                     recipient_list=[user.email],
    #                     fail_silently=False,
    #                 )

    #             self.message_user(request, "密碼已成功重設並發送到導師的郵箱。",
    #                               level=messages.SUCCESS)
    #             return redirect(f'../../{object_id}/change/')
    #     else:
    #         form = MentorPasswordResetForm()

    #     context = dict(
    #         self.admin_site.each_context(request),
    #         title='重設導師密碼',
    #         mentor=mentor,
    #         form=form,
    #         opts=self.model._meta,
    #         original=mentor,
    #         save_as=False,
    #         has_view_permission=self.has_view_permission(request, mentor),
    #         has_change_permission=self.has_change_permission(request, mentor),
    #         has_add_permission=self.has_add_permission(request),
    #         has_delete_permission=self.has_delete_permission(request, mentor),
    #         has_editable_inline_admin_formsets=False,
    #     )
    #     return TemplateResponse(request, "admin/mentor/reset_pw.html", context)
