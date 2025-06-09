from .models import Student, StudentSession, Grade
from django.contrib import admin


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    search_fields = ['name']  # required for autocomplete


@admin.register(StudentSession)
class StudentSessionAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'session_id')
    list_display = ('get_user_id', 'session_id')

    def get_user_id(self, obj):
        return obj.user.user_id
    get_user_id.short_description = 'User ID'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['parent', 'grade', 'school']

    list_display = (
        'id',
        'strn',
        'id_no',
        'chinese_name',
        'english_name',
        'school',
        'grade',
        'date_of_birth',
        'parent_info',  # custom method here
    )

    def parent_info(self, obj):
        parent = obj.parent
        if not parent:
            return "-"
        # Customize field names below according to your user model
        phone = getattr(parent, 'phone', '')
        email = getattr(parent, 'email', '')
        name = getattr(parent, 'name', '') or getattr(
            parent, 'get_full_name', lambda: '')()
        user_id = getattr(parent, 'id', '')
        return f"{name} | {phone} | {email} | ID: {user_id}"

    parent_info.short_description = "家長資訊"
    # Optional: allow sorting by parent id
    parent_info.admin_order_field = 'parent__id'

    # Optional filters and search
    list_filter = ('school', 'grade', 'parent')
    search_fields = ('chinese_name', 'english_name', 'strn',
                     'id_no', 'parent__name', 'parent__email')
