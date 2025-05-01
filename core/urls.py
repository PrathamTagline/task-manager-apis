from django.urls import path

from core.views import dashboard_page_view

urlpatterns = [
    path("dashboard/", dashboard_page_view, name="dashboard"),
]
