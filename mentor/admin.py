import random
import string
from django import forms
from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Mentor

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
