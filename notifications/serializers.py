from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.StringRelatedField(read_only=True)  # shows recipient email
    sender = serializers.StringRelatedField(read_only=True)  # shows sender email

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'sender',
            'notification_type',
            'title',
            'message',
            'is_read',
            'is_online',
            'created_at',
            'project',
            'task',
        ]
        read_only_fields = ['id', 'recipient', 'sender', 'created_at']
