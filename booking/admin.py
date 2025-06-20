from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.urls import path
from .models import BookingStatus, Booking
from .forms import BookingAdminForm
from service.models import TimeSlot
from student.models import Student
from django.contrib.auth import get_user_model

User = get_user_model()


@staff_member_required
def get_timeslots(request):
    service_id = request.GET.get('service')
    if service_id:
        qs = TimeSlot.objects.filter(service_id=service_id)
    else:
        qs = TimeSlot.objects.none()  # Return nothing if no service selected
    timeslots = [{'id': ts.id, 'display': str(
        ts), 'service_id': ts.service_id} for ts in qs]
    return JsonResponse({'timeslots': timeslots})


@staff_member_required
def get_students_by_parent(request):
    parent_id = request.GET.get('parent_id')
    students = []
    if parent_id:
        # Use the user's primary key (id) to filter students
        students_qs = Student.objects.filter(parent__id=parent_id)
        students = [{'id': s.id, 'name': str(s)} for s in students_qs]
    return JsonResponse({'students': students})


@staff_member_required
def get_users_by_students(request):
    student_ids = request.GET.getlist('student_ids[]')
    users = []
    if student_ids:
        users_qs = User.objects.filter(students__id__in=student_ids).distinct()
        users = [{'id': u.id, 'name': str(u)} for u in users_qs]
    return JsonResponse({'users': users})


@admin.register(BookingStatus)
class BookingStatusAdmin(admin.ModelAdmin):
    list_display = ('status',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm
    search_fields = ('service__name', 'user__email')
    list_display = ('user', 'service', 'time_slot', 'status', 'created_at')
    list_filter = (
        'status', ('service', admin.RelatedOnlyFieldListFilter), 'time_slot__status')
    autocomplete_fields = ['user', 'service', 'students']

    class Media:
        js = ('booking/js/booking_admin.js',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-timeslots/', self.admin_site.admin_view(get_timeslots),
                 name='get-timeslots'),
            path('get-students-by-parent/', self.admin_site.admin_view(
                get_students_by_parent), name='get-students-by-parent'),
            path('get-users-by-students/', self.admin_site.admin_view(
                get_users_by_students), name='get-users-by-students'),
        ]
        return custom_urls + urls
