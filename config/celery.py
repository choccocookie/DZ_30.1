import os
import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()
celery_app = Celery("config")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()


from celery.schedules import crontab
from django_celery_beat.models import PeriodicTask, IntervalSchedule

celery_app.conf.beat_schedule = {
    "check_inactive_users": {
        "task": "your_app.tasks.deactivate_inactive_users",
        "schedule": crontab(hour=0, minute=0),  # Раз в день в полночь
    },
}