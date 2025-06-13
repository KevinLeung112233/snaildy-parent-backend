from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'product_type',
        'price',
        'stock',
        'sku',
        'is_active',
        'created_at',
        'updated_at',
    )  # Fields shown in the list view

    list_filter = (
        'product_type',
        'is_active',
        'created_at',
        'updated_at',
    )  # Filters available in the sidebar

    search_fields = ('name', 'sku')  # Searchable fields

    ordering = ('-created_at', 'name')  # Default ordering

    # Read-only fields in the form
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'product_type',
                'price',
                'stock',
                'sku',
                'is_active',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
