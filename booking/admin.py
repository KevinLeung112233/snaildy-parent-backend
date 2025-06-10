from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.urls import path
from .models import BookingStatus, Booking
from .forms import BookingAdminForm
from service.models import TimeSlot


@staff_member_required
def get_timeslots(request):
    service_id = request.GET.get('service')
    if service_id:
        qs = TimeSlot.objects.filter(service_id=service_id)
    else:
        qs = TimeSlot.objects.all()  # Return all timeslots if no service selected
    timeslots = [{'id': ts.id, 'display': str(
        ts), 'service_id': ts.service_id} for ts in qs]
    return JsonResponse({'timeslots': timeslots})


@admin.register(BookingStatus)
class BookingStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm

    list_display = ('user', 'service', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'service', 'time_slot__status')
    autocomplete_fields = ['user', 'service']

    class Media:
        js = ('booking/js/booking_admin.js',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-timeslots/', self.admin_site.admin_view(get_timeslots),
                 name='get-timeslots'),
        ]

        return custom_urls + urls
