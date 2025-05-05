import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from asgi_middleware_static_file import ASGIMiddlewareStaticFile
from notifications.routes import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager_system.settings')
django.setup()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the base Django ASGI app
django_asgi_app = get_asgi_application()

# Correct usage with static_root_paths
django_asgi_app = ASGIMiddlewareStaticFile(
    django_asgi_app,
    static_url='/static',  # Define URL for static files
    static_root_paths=[os.path.join(BASE_DIR, 'staticfiles')]  # Global staticfiles directory
)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
