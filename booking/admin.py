from django.contrib import admin
from .models import BookingStatus, Booking


@admin.register(BookingStatus)
class BookingStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'service', 'time_slot__status')
