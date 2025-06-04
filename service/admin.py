from django.contrib import admin
from .models import Organization, Mentor, ServiceStatus, Service, TimeSlot


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'website', 'contact')


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')


@admin.register(ServiceStatus)
class ServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1
    classes = ['timeslot-inline']  # Add a CSS class for targeting


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'need_timeslot',
                    'status')
    inlines = [TimeSlotInline]

    class Media:
        # Custom JS file to control visibility
        js = ('service/js/hide_timeslot.js',)
