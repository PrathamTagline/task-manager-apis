# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

taskrouter = DefaultRouter()
taskrouter.register(r'projects/(?P<project_key>[^/]+)/tasks', TaskViewSet, basename='task')

subtasksrouter = DefaultRouter()
subtasksrouter.register(r'projects/(?P<project_key>[^/]+)/tasks/(?P<task_key>[^/]+)/subtasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(taskrouter.urls)),
    path('', include(subtasksrouter.urls)),
]
