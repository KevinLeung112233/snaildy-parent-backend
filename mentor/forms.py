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
