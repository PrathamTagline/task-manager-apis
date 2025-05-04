from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from task_manager_system import settings
from .views import ProjectViewSet,create_project,boarding_view,search_view,project_detail_view,all_project_view,test

router = DefaultRouter()
router.register(r'api/projects', ProjectViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('create/', create_project, name='create_project'),
    path('boarding/', boarding_view, name='boarding_page'),
    path('search/', search_view, name='search_page'),
    path("all/projects/",all_project_view,name="all-projects"),
    path("temp/search/", test, name=""),
    path('<str:key>/', project_detail_view, name='project_detail'),
]

# Serve media files during development (if DEBUG is True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
