from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Booking
from service.models import TimeSlot
from student.models import Student

User = get_user_model()


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'students': forms.SelectMultiple(attrs={
                'size': '100',  # controls dropdown height
                'style': 'width: 300px;',  # optional width styling
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set empty labels for ForeignKey fields
        self.fields['user'].empty_label = "Select a user"
        self.fields['time_slot'].empty_label = "Select a timeslot"

        # Filter user field to non-staff users only
        self.fields['user'].queryset = User.objects.filter(is_staff=False)

        # Filter time_slot queryset based on selected service
        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['time_slot'].queryset = TimeSlot.objects.filter(
                    service_id=service_id)
            except (ValueError, TypeError):
                self.fields['time_slot'].queryset = TimeSlot.objects.none()
        elif self.instance.pk and self.instance.service:
            self.fields['time_slot'].queryset = TimeSlot.objects.filter(
                service=self.instance.service)
        else:
            self.fields['time_slot'].queryset = TimeSlot.objects.all()

        # Determine the selected user (parent)
        user = None

        # When editing existing instance
        if self.instance and self.instance.pk:
            user = self.instance.user

        # When adding new instance and form data is submitted
        if 'user' in self.data:
            try:
                user_id = int(self.data.get('user'))
                user = User.objects.get(pk=user_id)
            except (ValueError, TypeError, User.DoesNotExist):
                user = None

        # Filter students queryset to include:
        # - students related to the selected user (parent)
        # - AND currently selected students on the instance (to show as selected)
        if user:
            qs = Student.objects.filter(parent=user)
            if self.instance.pk:
                qs = qs | self.instance.students.all()
            self.fields['students'].queryset = qs.distinct()
        else:
            self.fields['students'].queryset = Student.objects.none()

        if self.instance and self.instance.pk:
            self.fields['students'].initial = self.instance.students.all(
            ).values_list('pk', flat=True)

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        students = cleaned_data.get('students')

        # Validate that selected students belong to the user
        if user and students:
            invalid_students = [str(s) for s in students if s.parent != user]

            if invalid_students:
                raise ValidationError(
                    f"The following students do not belong to the selected user: {', '.join(invalid_students)}"
                )

        return cleaned_data
