from django.contrib import admin
from .models import StudentRecord, ParentRecord, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0  # Number of empty forms to display
    fields = ('file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'service', 'timeslot',
                    'attendance', 'created_at')
    inlines = [AttachmentInline]


@admin.register(ParentRecord)
class ParentRecordAdmin(admin.ModelAdmin):
    list_display = ('parent', 'service', 'timeslot',
                    'attendance', 'created_at')
    inlines = [AttachmentInline]
