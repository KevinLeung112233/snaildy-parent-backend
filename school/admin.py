from django.contrib import admin
from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('verbose_name_cn', 'verbose_name_eng', 'verbose_address',
                    'verbose_district', 'verbose_area', 'verbose_type')

    list_filter = ('district', 'area', 'type')
    search_fields = ('name_cn', 'name_eng', 'address')

    fields = ('name_cn', 'name_eng', 'address', 'district', 'area', 'type')

    @admin.display(description='中文名稱')
    def verbose_name_cn(self, obj):
        return obj.name_cn

    @admin.display(description='English Name')
    def verbose_name_eng(self, obj):
        return obj.name_eng

    @admin.display(description='地址')
    def verbose_address(self, obj):
        return obj.address

    @admin.display(description='區域')
    def verbose_district(self, obj):
        return obj.district

    @admin.display(description='地區')
    def verbose_area(self, obj):
        return obj.area

    @admin.display(description='類別')
    def verbose_type(self, obj):
        return obj.type
