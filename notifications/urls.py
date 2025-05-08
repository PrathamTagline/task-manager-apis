from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

# Create DRF router
router = DefaultRouter()
router.register(r'api/notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
