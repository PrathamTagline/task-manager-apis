import os
from uuid import UUID
import django
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Notification
from django.db import DatabaseError
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_system.settings')
django.setup()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Mark user as online in all unread notifications
        await self.mark_user_online(True)

        logger.info(f"User {self.user_id} connected to WebSocket")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.mark_user_online(False)

        logger.info(f"User {self.user_id} disconnected with code: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        logger.info(f"Received data from user {self.user_id}: {data}")

        # Optional: process client-sent data (like mark notifications as read)

        await self.send(text_data=json.dumps({'status': 'received'}))

    async def send_notification(self, event):
        notification_data = event['notification']

        # Save notification to database
        saved_notification = await self.save_notification(notification_data)

        # Serialize saved notification to JSON for client
        serialized_data = {
            'id': saved_notification.id,
            'title': saved_notification.title,
            'message': saved_notification.message,
            'notification_type': saved_notification.notification_type,
            'is_read': saved_notification.is_read,
            'is_online': saved_notification.is_online,
            'created_at': saved_notification.created_at.isoformat()
        }

        await self.send(text_data=json.dumps(serialized_data))

    @sync_to_async
    def save_notification(self, notification_data):
        try:
            # Convert the recipient and sender to UUID if they are strings
            recipient_id = UUID(notification_data.get('recipient'))
            sender_id = UUID(notification_data.get('sender'))
            
            # Ensure all necessary fields are present in notification_data
            if not recipient_id or not sender_id:
                raise ValueError("Recipient ID or Sender ID is missing or invalid")
            
            # Add converted UUIDs to notification_data
            notification_data['recipient'] = recipient_id
            notification_data['sender'] = sender_id
            
            # Proceed with saving the notification
            notification = Notification.objects.create(**notification_data)
            logger.info(f"Saved notification ID {notification.id} for user {self.user_id}")
            return notification
        except DatabaseError as e:
            logger.error(f"Database error while saving notification: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None


    @sync_to_async
    def mark_user_online(self, online_status):
        # Updates all unread notifications for the user to mark is_online
        Notification.objects.filter(recipient_id=self.user_id, is_read=False).update(is_online=online_status)
