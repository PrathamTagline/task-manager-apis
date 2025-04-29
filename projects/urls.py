from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)


urlpatterns = [
    path('', include(router.urls)),
     # Explicitly define the member detail URL
    path('projects/<str:key>/member/<str:member_id>/', 
         ProjectViewSet.as_view({'get': 'get_member_by_id', 'patch': 'update_member', 'delete': 'remove_member'}),
         name='project-member-detail'),
    
    # Other explicit URLs if needed
    path('projects/<str:key>/members/', 
         ProjectViewSet.as_view({'get': 'members'}),
         name='project-members-list'),
    
    path('projects/<str:key>/add_member/', 
         ProjectViewSet.as_view({'post': 'add_member'}),
         name='project-add-member'),
    
    path('projects/<str:key>/member/email/<str:email>/', 
         ProjectViewSet.as_view({'get': 'get_member_by_email'}),
         name='project-member-by-email'),
]

# The following endpoints are available through the viewset actions:

# Project membership-related endpoints:
# GET /projects/{project_key}/members/ - List all members for a project
# POST /projects/{project_key}/add_member/ - Add a new member to a project
# GET /projects/{project_key}/member/{member_id}/ - Get member details by ID
# GET /projects/{project_key}/member/email/{email}/ - Get member details by email
# PATCH /projects/{project_key}/member/{member_id}/ - Update member role
# DELETE /projects/{project_key}/member/{member_id}/ - Remove a member

# Standard project-related endpoints:
# GET /projects/ - List all projects for the current user
# POST /projects/ - Create a new project
# GET /projects/{project_key}/ - Get project details
# PUT/PATCH /projects/{project_key}/ - Update project
# DELETE /projects/{project_key}/ - Delete project

# Standard membership-related endpoints:
# GET /memberships/ - List all memberships for the current user
# POST /memberships/ - Create a new membership
# GET /memberships/{id}/ - Get membership details
# PUT/PATCH /memberships/{id}/ - Update membership
# DELETE /memberships/{id}/ - Delete membership