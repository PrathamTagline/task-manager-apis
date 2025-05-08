from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Notification(models.Model):
    """
    Model for storing user notifications.
    """
    NOTIFICATION_TYPES = (
        ('TASK_ASSIGNED', 'Task Assigned'),
        ('TASK_UPDATED', 'Task Updated'),
        ('TASK_COMPLETED', 'Task Completed'),
        ('PROJECT_INVITE', 'Project Invite'),
        ('COMMENT_ADDED', 'Comment Added'),
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_notifications'
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='TASK_ASSIGNED'  # ✅ add a default
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    is_read = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)  # ✅ ADDED FIELD

    created_at = models.DateTimeField(auto_now_add=True)  # (already exists)

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.notification_type} - {self.recipient.email}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])
