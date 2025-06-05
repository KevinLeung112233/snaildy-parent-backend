from django.apps import AppConfig
from django.contrib import admin
from django.apps import apps


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        HIDE_MODELS = [
            ('account', 'EmailAddress'),
            ('auth', 'Group'),
            ('socialaccount', 'SocialAccount'),
            ('socialaccount', 'SocialApp'),
            ('socialaccount', 'SocialToken'),
        ]

        for app_label, model_name in HIDE_MODELS:
            try:
                model = apps.get_model(app_label, model_name)
                admin.site.unregister(model)
            except (admin.sites.NotRegistered, LookupError):
                pass
