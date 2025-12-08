from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class StudentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "students"

    def ready(self):
        # Import here so apps are loaded before touching auth models
        from django.contrib.auth.models import update_last_login

        # Disable last_login DB writes (helps on read-only environments like Vercel+SQLite)
        user_logged_in.disconnect(update_last_login)
