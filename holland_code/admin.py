from django.contrib import admin
from .models import HollandCode


@admin.register(HollandCode)
class HollandCodeAdmin(admin.ModelAdmin):
    list_display = ('student', 'first_code',
                    'second_code', 'third_code', 'date')
    list_filter = ('first_code', 'second_code', 'third_code', 'date')
    # Use related field lookup for student
    search_fields = ('student__chinese_name', 'first_code',
                     'second_code', 'third_code')
    ordering = ('-date',)

    fieldsets = (
        (None, {
            'fields': ('student', 'first_code', 'second_code', 'third_code', 'date')
        }),
    )
