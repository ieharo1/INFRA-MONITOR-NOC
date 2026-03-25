import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infra_monitor.settings')

app = Celery('infra_monitor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'monitor-all-services-every-60s': {
        'task': 'monitoring.tasks.run_monitoring_cycle',
        'schedule': 60.0,
    }
}
