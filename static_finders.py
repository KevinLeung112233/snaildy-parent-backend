# snaildy_parent_backend/static_finders.py
from django.contrib.staticfiles.finders import AppDirectoriesFinder
from django.utils._os import safe_join


class GrappelliFinder(AppDirectoriesFinder):
    """
    A static files finder that looks in the grappelli directory first.
    """

    def find_in_app(self, app, path):
        if app == 'grappelli':
            return super().find_in_app(app, path)
        return None

    def list(self, ignore_patterns):
        for app in ['grappelli']:
            app_storage = self.storages.get(app)
            if app_storage:
                for path in self.list_files(app_storage, ignore_patterns):
                    yield path, app_storage
