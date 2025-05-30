# urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def static_files_debug(request):
    from django.contrib.staticfiles.finders import find
    grappelli_files = {
        'jquery.min.js': find('grappelli/jquery/jquery.min.js'),
        'jquery-ui.min.css': find('grappelli/jquery/ui/jquery-ui.min.css'),
        'screen.css': find('grappelli/stylesheets/screen.css'),
    }
    return JsonResponse(grappelli_files)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('static-debug/', static_files_debug),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
