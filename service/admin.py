from django.contrib import admin
from .models import Organization, ServiceStatus, Service, TimeSlot, ServiceType
# from rangefilter.filters import DateRangeFilter
from django import forms


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


@admin.register(ServiceStatus)
class ServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('display_name_cn',)

    def display_name_cn(self, obj):
        return obj.display_name
    display_name_cn.short_description = "服務狀態"


# class TimeSlotInlineForm(forms.ModelForm):
#     class Meta:
#         model = TimeSlot
#         fields = '__all__'
#         widgets = {
#             'start_datetime': forms.TextInput(attrs={'class': 'datetimepicker'}),
#             'end_datetime': forms.TextInput(attrs={'class': 'datetimepicker'}),
#         }


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    # form = TimeSlotInlineForm
    extra = 1
    fields = (
        'start_datetime',
        'end_datetime',
        'capacity',
        'status',
        'current_headcount',
    )
    classes = ['collapse', 'timeslot-inline']

    # class Media:
    #     css = {
    #         'all': ('https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',)
    #     }
    #     js = (
    #         'https://cdn.jsdelivr.net/npm/flatpickr',
    #         'https://cdn.jsdelivr.net/npm/flatpickr/dist/plugins/confirmDate/confirmDate.js',
    #         '/static/service/js/init_flatpickr.js',  # your custom JS to init flatpickr
    #     )


class CustomServiceAdmin(admin.ModelAdmin):
    class Media:
        js = ('service/js/remove_autofocus.js',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name_cn', 'status_display_name_cn', 'price', 'expiry_date',
        'period_start', 'period_end', 'mentors_cn', 'organization'
    )
    autocomplete_fields = ('mentors',)  # works without importing Mentor
    list_filter = ('status',)
    ordering = (
        'id', 'expiry_date', 'period_start', 'period_end',
        'mentors', 'organization', 'name'
    )

    search_fields = [
        'id',
        'name',
        'organization__name',
        'mentors__name',
    ]

    # Assuming you have TimeSlotInline defined somewhere
    inlines = [TimeSlotInline]

    def name_cn(self, obj):
        return obj.name
    name_cn.short_description = "名稱"

    def mentors_cn(self, obj):
        return ", ".join(mentor.name for mentor in obj.mentors.all())
    mentors_cn.short_description = "導師"

    def status_display_name_cn(self, obj):
        return obj.status.display_name if obj.status else "-"
    status_display_name_cn.short_description = "狀態"

    def get_fields(self, request, obj=None):
        return [
            'expiry_date', 'name', 'detail', 'price', 'deposit_percentage', 'price_desc',
            'location', 'type', 'capacity', 'organization', 'mentors', 'status',
            'promote_label', 'period_start', 'period_end',
            'free_accompanying_children', 'extra_child_fee',
            'min_selection', 'max_selection',
        ]


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def __str__(self):
        return self.name
