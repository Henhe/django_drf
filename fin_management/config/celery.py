from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("fin_management")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.task_queues = {
    "high_priority": {
        "exchange": "high_priority",
        "routing_key": "high",
    },
    "default": {
        "exchange": "default",
        "routing_key": "default",
    },
    "low_priority": {
        "exchange": "low_priority",
        "routing_key": "low",
    }
}

app.conf.task_default_exchange = "default"
app.conf.task_default_routing_key = "default"
app.conf.task_default_queue = "default"
