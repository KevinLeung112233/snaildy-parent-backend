from django import forms
from django.contrib.auth import get_user_model
from .models import Booking
from service.models import TimeSlot

User = get_user_model()


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            self.fields['time_slot'].queryset = TimeSlot.objects.none()
