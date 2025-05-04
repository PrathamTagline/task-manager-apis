# views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from urllib.parse import unquote

from .models import Project, ProjectMembership
from .serializers import ProjectSerializer, ProjectMembershipSerializer
from accounts.models import User
from django.http import HttpResponse

class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Projects and their Memberships.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'key'

    def get_queryset(self):
        """
        Filter projects by current user's created or member projects.
        Supports optional filters: name, search, type.
        """
        user = self.request.user
        queryset = Project.objects.filter(
            Q(created_by=user) | Q(memberships__user__email=user)
        ).distinct()

        name = self.request.query_params.get('name')
        search = self.request.query_params.get('search')
        project_type = self.request.query_params.get('type')
        project_key = self.request.query_params.get('key')
        email = self.request.query_params.get('email')
        
        if project_key:
            queryset = queryset.filter(key__iexact=project_key)

        if name:
            queryset = queryset.filter(name__iexact=name)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        if project_type:
            queryset = queryset.filter(type__iexact=project_type)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new Project and add creator as Admin in memberships.
        """
        user = request.user
        data = request.data

        project = Project.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            type=data.get('type'),
            created_by=user,
        )
        ProjectMembership.objects.create(project=project, user=user, role='Admin')

        serializer = self.get_serializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve project details along with owner and memberships info.
        """
        project = self.get_object()
        project_data = self.get_serializer(project).data

        owner = project.created_by
        owner_data = {
            "id": owner.id,
            "username": owner.username,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email,
            "profile_image": owner.profile_image.url if owner.profile_image and hasattr(owner.profile_image, 'url') else None,
        }

        memberships_data = [
            {
                "id": membership.id,
                "user": {
                    "id": membership.user.id,
                    "username": membership.user.username,
                    "first_name": membership.user.first_name,
                    "last_name": membership.user.last_name,
                    "email": membership.user.email,
                    "profile_image": membership.user.profile_image.url if membership.user.profile_image and hasattr(membership.user.profile_image, 'url') else None,
                },
                "role": membership.role,
                "joined_at": membership.joined_at,
            }
            for membership in project.memberships.all()
        ]

        project_data.update({
            'owner': owner_data,
            'memberships': memberships_data,
            'created_by': owner_data,
            'created_at': project.created_at,
            'type': project.type,
        })

        return Response(project_data)
    
    def update(self, request, *args, **kwargs):
        """
        Update a project.
        Only the project owner can perform this action.
        """
        project = self.get_object()

        # Check if the requesting user is the project owner
        if request.user != project.created_by:
            raise PermissionDenied(detail="Only the project owner can update this project.")

        # Perform the update
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(project, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a project.
        Only the project owner can perform this action.
        """
        project = self.get_object()

        # Check if the requesting user is the project owner
        if request.user != project.created_by:
            raise PermissionDenied(detail="Only the project owner can delete this project.")

        # Delete the project
        self.perform_destroy(project)
        return Response({"detail": "Project deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    # ------------------- Membership Actions -------------------

    @action(detail=True, methods=['get'], url_path='memberships/all')
    def get_all_memberships(self, request, key=None):
        project = self.get_object()
        memberships = ProjectMembership.objects.filter(project=project)
        serializer = ProjectMembershipSerializer(memberships, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['post'], url_path='memberships/add')
    def add_membership(self, request, key=None):
        """
        Add a user to a project by email.
        Only Admins or Project Owners can perform this action.
        """
        project = self.get_object()
        self._check_admin_or_owner(request.user, project)

        email = request.data.get('email')
        role = request.data.get('role', 'Member')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if ProjectMembership.objects.filter(project=project, user=user).exists():
            return Response({"detail": "User is already a member."}, status=status.HTTP_400_BAD_REQUEST)

        if role not in dict(ProjectMembership.ROLE_CHOICES):
            return Response({"detail": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

        ProjectMembership.objects.create(project=project, user=user, role=role)
        return Response({"detail": "Membership created successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='memberships/remove')
    def remove_membership(self, request, key=None):
        """
        Remove a user from a project by email.
        Only Admins or Project Owners can perform this action.
        """
        project, membership = self._get_project_membership_by_email('remove', request.data.get('email'))
        self._check_admin_or_owner(request.user, project)

        if not membership:
            return Response({"detail": "Membership not found."}, status=status.HTTP_404_NOT_FOUND)

        membership.delete()
        return Response({"detail": "Membership removed successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['put'], url_path='memberships/update')
    def update_membership(self, request, key=None):
        """
        Update a user's role in a project by email.
        Only Admins or Project Owners can perform this action.
        """
        project, membership = self._get_project_membership_by_email('update', request.data.get('email'))
        self._check_admin_or_owner(request.user, project)

        if not membership:
            return Response({"detail": "Membership not found."}, status=status.HTTP_404_NOT_FOUND)

        role = request.data.get('role')
        if role not in dict(ProjectMembership.ROLE_CHOICES):
            return Response({"detail": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

        membership.role = role
        membership.save()
        return Response({"detail": "Membership updated successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='memberships')
    def get_memberships(self, request, key=None):
        """
        Retrieve memberships of a project by role or email.
        Only Admins or Project Owners can perform this action.
        """
        project = self.get_object()
        self._check_admin_or_owner(request.user, project)

        # Check for 'role' query parameter
        role = request.query_params.get('role')
        if role:
            memberships = ProjectMembership.objects.filter(project=project, role=role)
            serializer = ProjectMembershipSerializer(memberships, many=True)
            return Response(serializer.data)

        # Check for 'email' query parameter
        email = request.query_params.get('email')
        if email:
            try:
                user = User.objects.get(email=unquote(email))
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            membership = ProjectMembership.objects.filter(project=project, user=user).first()
            if not membership:
                return Response({"detail": "Membership not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProjectMembershipSerializer(membership)
            return Response(serializer.data)

        # If neither 'role' nor 'email' is provided
        return Response({"detail": "Either 'role' or 'email' query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    

    def _check_admin_or_owner(self, user, project):
        """
        Ensure the user is either an Admin or the Project Owner.
        """
        if user == project.created_by:
            return
        membership = ProjectMembership.objects.filter(project=project, user=user).first()
        if not membership or membership.role != 'Admin':
            raise PermissionDenied(detail="Only Admins or Project Owners can perform this action.")

    def _get_project_membership_by_email(self, key, email):
        """
        Helper to retrieve project and membership by key and user email.
        """
        project = self.get_object()
        user = get_object_or_404(User, email=unquote(email))
        membership = ProjectMembership.objects.filter(project=project, user=user).first()
        if not membership:
            raise NotFound(detail="Membership not found.")

        return project, membership



def project_detail_view(request, key):
    return render(request, 'projects/boarding_page.html', {'key': key})

def create_project(request):
    return render(request, 'projects/create_project_page.html')

def boarding_view(request):
    return render(request, 'projects/boarding_page.html')

def search_view(request):
    return render(request, 'projects/search_bar.html')

def all_project_view(request):
    return render(request,"projects/all_projects_page.html")


def test(request):
   return render(request,"projects/test.html")