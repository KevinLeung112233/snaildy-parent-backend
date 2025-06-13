from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount_amount',
        'discount_percent',
        'valid_from',
        'valid_to',
        'active',
        'quota',
        'used_count',
        'user_quota',
        'display_users',
    )

    list_filter = (
        'active',
        'valid_from',
        'valid_to',
        'quota',
        'user_quota',
        'users',
    )

    search_fields = ('code',)
    ordering = ('-valid_to', 'code')

    def display_users(self, obj):
        # Show a comma-separated list of usernames or emails for allowed users
        return ", ".join([str(user) for user in obj.users.all()])
    display_users.short_description = '指定用戶'

    readonly_fields = ('used_count',)

    fieldsets = (
        (None, {
            'fields': (
                'code',
                'discount_amount',
                'discount_percent',
                'valid_from',
                'valid_to',
                'active',
            )
        }),
        ('Usage Limits', {
            'fields': (
                'quota',
                'used_count',
                'user_quota',
                'users',
            )
        }),
    )
