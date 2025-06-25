# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from booking.admin import get_timeslots  # import your view


def static_files_debug(request):
    from django.contrib.staticfiles.finders import find
    grappelli_files = {
        'jquery.min.js': find('grappelli/jquery/jquery.min.js'),
        'jquery-ui.min.css': find('grappelli/jquery/ui/jquery-ui.min.css'),
        'screen.css': find('grappelli/stylesheets/screen.css'),
    }
    return JsonResponse(grappelli_files)


urlpatterns = [
    # Grappelli URLS must come BEFORE admin URLs
    path('grappelli/', include('grappelli.urls')),
    # path('admin/booking/get-timeslots/',
    #      staff_member_required(get_timeslots), name='get-timeslots'),
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # Your other URL patterns
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('student.urls')),
    path('api/v1/', include('school.urls')),
]


if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
