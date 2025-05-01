from django.urls import path

from core.views import dashboard_page_view, home_view

urlpatterns = [
    path('', home_view, name='home_page'),
    path("dashboard/", dashboard_page_view, name="dashboard"),
]
