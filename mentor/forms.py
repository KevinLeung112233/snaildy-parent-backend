from django import forms
from .models import Mentor
from django.contrib.auth import get_user_model

User = get_user_model()


class MentorAdminForm(forms.ModelForm):
    class Meta:
        model = Mentor
        # No phone field here, only other Mentor fields if any
        fields = []


class MentorUserCreationForm(forms.ModelForm):
    # No password fields here, password will be set in save()
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'login_method')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set password outside the form, e.g., in admin.save_model()
        if commit:
            user.save()
        return user


class MentorPasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the new password."
    )
    password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password again for confirmation."
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError(
                "The two password fields didn’t match.")
        return cleaned_data
