# task_manager_system/asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from notifications.routes import websocket_urlpatterns  # Import from notifications app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_system.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)  # Use imported WebSocket URLs
    ),
})
