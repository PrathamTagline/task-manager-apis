# notifications/routes.py

from django.urls import re_path
from . import consumers

# Define dynamic WebSocket route with project key
websocket_urlpatterns = [
    # Dynamic route to handle different project keys (e.g., "PA", "NP")
    re_path(r'ws/project/(?P<project_key>\w+)/$', consumers.ProjectConsumer.as_asgi()),
]
