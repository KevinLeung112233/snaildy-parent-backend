from .models import Student
from django.contrib import admin
from .models import StudentSession


@admin.register(StudentSession)
class StudentSessionAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'session_id')
    list_display = ('get_user_id', 'session_id')

    def get_user_id(self, obj):
        return obj.user.user_id
    get_user_id.short_description = 'User ID'


admin.site.register(Student)
