from django.contrib import admin
from .models import SubscriptionPlan, SubscriptionPlanPrice, Subscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'billing_cycle', 'duration_days', 'is_active')
    list_filter = ('billing_cycle', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('id',)
    inlines = []


@admin.register(SubscriptionPlanPrice)
class SubscriptionPlanPriceAdmin(admin.ModelAdmin):
    list_display = ('plan', 'member_tier', 'price')
    list_filter = ('plan', 'member_tier')
    search_fields = ('plan__name', 'member_tier__name')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date',
                    'status', 'auto_renew', 'is_active')
    list_filter = ('status', 'auto_renew', 'plan__billing_cycle')
    search_fields = ('user__email', 'user__phone_number', 'plan__name')
    raw_id_fields = ('user', 'plan', 'payment')
    date_hierarchy = 'start_date'

    def is_active(self, obj):
        return obj.is_active()
    is_active.boolean = True
    is_active.short_description = '有效'

# Optional: Add SubscriptionPlanPrice inline in SubscriptionPlan admin for easier management


class SubscriptionPlanPriceInline(admin.TabularInline):
    model = SubscriptionPlanPrice
    extra = 1


SubscriptionPlanAdmin.inlines = [SubscriptionPlanPriceInline]
