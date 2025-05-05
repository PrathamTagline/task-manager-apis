# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from projects.models import ProjectMembership
from notifications.utils import notify_project_members

@receiver(post_save, sender=ProjectMembership)
def notify_on_member_added(sender, instance, created, **kwargs):
    if created:
        message = f"{instance.user.get_full_name()} was added to the project as {instance.role}."
        notify_project_members(instance.project.key, message)
