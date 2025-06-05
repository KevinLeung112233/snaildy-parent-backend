from django.contrib import admin
from .models import Organization, Mentor, ServiceStatus, Service, TimeSlot


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name_cn', 'phone_cn', 'website_cn', 'contact_cn')

    def name_cn(self, obj):
        return obj.name
    name_cn.short_description = "名稱"

    def phone_cn(self, obj):
        return obj.phone
    phone_cn.short_description = "電話"

    def website_cn(self, obj):
        return obj.website
    website_cn.short_description = "網站"

    def contact_cn(self, obj):
        return obj.contact
    contact_cn.short_description = "聯絡人"


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email')
    list_display = ('name_cn', 'email_cn', 'phone_cn')

    def name_cn(self, obj):
        return obj.name
    name_cn.short_description = "導師名稱"

    def email_cn(self, obj):
        return obj.email
    email_cn.short_description = "電子郵件"

    def phone_cn(self, obj):
        return obj.phone
    phone_cn.short_description = "電話"


@admin.register(ServiceStatus)
class ServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('display_name_cn',)

    def display_name_cn(self, obj):
        return obj.display_name
    display_name_cn.short_description = "服務狀態"


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1
    fields = (
        'start_datetime',
        'capacity',
        'status',
        'current_headcount',
    )
    classes = ['timeslot-inline']
    readonly_fields = ('current_headcount',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_cn', 'mentors_cn', 'status_display_name_cn')
    autocomplete_fields = ('mentors',)
    inlines = [TimeSlotInline]  # Always show inline

    def name_cn(self, obj):
        return obj.name
    name_cn.short_description = "名稱"

    def mentors_cn(self, obj):
        return ", ".join(mentor.name for mentor in obj.mentors.all())
    mentors_cn.short_description = "導師"

    def status_display_name_cn(self, obj):
        return obj.status.display_name if obj.status else "-"
    status_display_name_cn.short_description = "Stauts"

    def get_fields(self, request, obj=None):
        fields = [
            'expiry_date', 'name', 'detail', 'price', 'price_desc', 'location', 'capacity',
            'organization', 'mentors', 'status', 'promote_label',
            'period_start', 'period_end',
            'min_selection',
            'max_selection',
        ]
        return fields
