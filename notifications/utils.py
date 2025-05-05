from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_project_members(project_key, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"project_{project_key}",
        {
            "type": "send_notification",
            "message": message,
        }
    )
