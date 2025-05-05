import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_key = self.scope['url_route']['kwargs']['project_key']
        self.room_name = f'project_{self.project_key}'  # Unique room for each project
        self.room_group_name = f'project_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Send message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            print("Received invalid JSON or empty message.")    
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format. Expected JSON.'
            }))
        except KeyError:
            print("Received JSON without 'message' key.")
            await self.send(text_data=json.dumps({
                'error': 'Missing "message" key in JSON.'
            }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # New method to handle project notifications
    async def send_project_notification(self, notification_message):
        # Send a notification to all members of the project
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': notification_message
            }
        )
