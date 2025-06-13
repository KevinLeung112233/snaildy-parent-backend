from django.contrib import admin
from .models import SenType, SenLevel, SenStatus, Sen


@admin.register(SenType)
class SenTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SenLevel)
class SenLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SenStatus)
class SenStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Sen)
class SenAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'sen_type', 'level',
                    'status', 'created_at', 'updated_at')
    list_filter = ('sen_type', 'level', 'status')
    search_fields = ('student_id',)
    ordering = ('-created_at',)
