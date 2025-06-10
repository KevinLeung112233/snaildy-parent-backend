from django.contrib import admin
from .models import StudentRecord, ParentRecord, Attachment
from mentor.models import Mentor


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    fields = ('file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'service', 'timeslot',
                    'attendance', 'created_at')
    inlines = [AttachmentInline]

    def has_module_permission(self, request):
        user = request.user
        return user.is_superuser or getattr(user, 'is_mentor', False)

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.is_superuser:
            return qs

        if getattr(user, 'is_mentor', False):
            try:
                mentor = user.mentor_profile  # use related_name from Mentor.user field
            except Mentor.DoesNotExist:
                return qs.none()

            return qs.filter(service__mentors=mentor).distinct()

        return qs.none()


@admin.register(ParentRecord)
class ParentRecordAdmin(admin.ModelAdmin):
    list_display = ('parent', 'service', 'timeslot',
                    'attendance', 'created_at')
    inlines = [AttachmentInline]

    def has_module_permission(self, request):
        user = request.user
        return user.is_superuser or getattr(user, 'is_mentor', False)

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.is_superuser:
            return qs

        if getattr(user, 'is_mentor', False):
            try:
                mentor = user.mentor_profile
            except Mentor.DoesNotExist:
                return qs.none()

            return qs.filter(service__mentors=mentor).distinct()

        return qs.none()
