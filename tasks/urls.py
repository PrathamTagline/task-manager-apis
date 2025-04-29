# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'projects/(?P<project_key>[^/]+)/tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
