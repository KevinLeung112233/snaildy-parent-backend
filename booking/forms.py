from django import forms
from django.contrib.auth import get_user_model
from .models import Booking
from service.models import TimeSlot
from student.models import Student
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget, Select2MultipleWidget

User = get_user_model()


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        # widgets = {
        #     'user': Select2Widget,        # single select
        #     'students': Select2MultipleWidget,  # multiple select
        #     'service': Select2Widget,
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set empty labels
        self.fields['user'].empty_label = "Select a user"
        self.fields['time_slot'].empty_label = "Select a timeslot"

        # Filter user field to non-staff users only
        self.fields['user'].queryset = User.objects.filter(is_staff=False)

        # Filter time_slot based on selected service
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
            # Show all timeslots initially
            self.fields['time_slot'].queryset = TimeSlot.objects.all()

        # Filter students based on selected user
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

        if user:
            self.fields['students'].queryset = Student.objects.filter(
                parent=user)
        else:
            # Show no students when no user is selected
            self.fields['students'].queryset = Student.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        students = cleaned_data.get('students')

        # Validate that selected students belong to the user
        if user and students:
            invalid_students = []
            for student in students:
                if student.parent != user:
                    invalid_students.append(str(student))

            if invalid_students:
                raise ValidationError(
                    f"The following students do not belong to the selected user: {', '.join(invalid_students)}"
                )

        return cleaned_data
