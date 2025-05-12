# task_manager_system/celery.py

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_system.settings')

app = Celery('task_manager_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'send-reminders-every-hour': {
        'task': 'task_app.tasks.send_due_task_reminders',
        'schedule': crontab(minute=0, hour='*'),  # every hour
    },
}
