import os
import django
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification
from asgiref.sync import sync_to_async
from django.db import DatabaseError
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_system.settings')
django.setup()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with code: {close_code}")
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']

            # Save to database (wrap sync DB call)
            await self.save_notification(message)

            await self.channel_layer.group_send(
                "notifications",
                {
                    'type': 'send_notification',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON data'
            }))
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Error processing message'
            }))

    @sync_to_async
    def save_notification(self, message):
        try:
            notification = Notification.objects.create(message=message)
            return notification
        except DatabaseError as e:
            logger.error(f"Database error while saving notification: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error saving notification: {str(e)}")
            raise

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
