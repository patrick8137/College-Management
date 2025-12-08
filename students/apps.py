from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import update_last_login

class StudentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "students"

    def ready(self):
        # ✅ Prevent Django from writing last_login to DB (Vercel SQLite fix)
        user_logged_in.disconnect(update_last_login)
