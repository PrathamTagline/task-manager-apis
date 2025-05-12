# task_app/tasks.py
import os 
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task
import environ
from django.conf import settings

base_dir = settings.BASE_DIR
env = environ.Env()
environ.Env.read_env(os.path.join(base_dir, '.env'))
@shared_task
def send_task_notification(task_id):
    task = Task.objects.get(id=task_id)
    send_mail(
        subject=f"Task Notification: {task.title}",
        message=f"Hi {task.assigned_to}, you have a new/updated task: {task.title}",
        from_email= env('EMAIL_HOST_USER'),
        recipient_list=[task.assigned_to.email],
        fail_silently=False,
    )

@shared_task
def send_due_task_reminders():
    now = timezone.now()
    upcoming_tasks = Task.objects.filter(
        deadline__lte=now + timezone.timedelta(hours=1),
        is_completed=False
    )
    for task in upcoming_tasks:
        send_mail(
            subject=f"Reminder: Task '{task.title}' is due soon!",
            message=f"Your task '{task.title}' is due at {task.deadline}. Please complete it on time.",
            from_email=env('EMAIL_HOST_USER'),
            recipient_list=[task.assigned_to.email],
            fail_silently=False,
        )
