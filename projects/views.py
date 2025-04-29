from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
from django.shortcuts import get_object_or_404
from urllib.parse import unquote

from .models import Project, ProjectMembership
from .serializers import ProjectSerializer, ProjectMembershipSerializer
from accounts.models import User


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing projects and their memberships.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'key'

    def get_queryset(self):
        """
        Optionally filter projects based on query parameters.
        """
        user = self.request.user
        queryset = Project.objects.filter(
            Q(created_by=user) | Q(memberships__user=user)
        ).distinct()

        name = self.request.query_params.get('name')
        search = self.request.query_params.get('search')
        project_type = self.request.query_params.get('type')

        if name:
            queryset = queryset.filter(name__iexact=name)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if project_type:
            queryset = queryset.filter(type__iexact=project_type)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new project and add the creator as Admin.
        """
        user = request.user
        data = request.data

        project = Project.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            type=data.get('type'),
            created_by=user
        )
        project.memberships.create(user=user, role='Admin')

        serializer = self.get_serializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='memberships')
    def get_memberships(self, request, key=None):
        """
        Get all memberships for a project.
        """
        project = self.get_object()
        memberships = ProjectMembership.objects.filter(project=project)
        serializer = ProjectMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='memberships/add')
    def add_membership(self, request, key=None):
        """
        Add a user to the project by email.
        Only Admins or Project Owners can add.
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

    @action(detail=True, methods=['get'], url_path='memberships/<str:email>')
    def get_membership_by_email(self, request, key=None, email=None):
        """
        Retrieve a membership by the user's email.
        """
        project = self.get_object()  # Get the project object using the key passed in the URL
        
        # Check if the user exists by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No User matches the given email."}, status=status.HTTP_404_NOT_FOUND)
        
        # Filter the ProjectMembership by project key and user email
        membership = ProjectMembership.objects.filter(project__key=key, user=user).first()
        
        # If no membership is found
        if not membership:
            return Response({"detail": "Membership not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the membership and return it
        serializer = ProjectMembershipSerializer(membership)
        return Response(serializer.data)


    @action(detail=True, methods=['put'], url_path='memberships/(?P<email>[^/.]+)/update')
    def update_membership_role_by_email(self, request, key=None, email=None):
        """
        Update the role of a membership by the user's email.
        """
        project = self.get_object()
        decoded_email = unquote(email)
        try:
            user = User.objects.get(email=decoded_email)
        except User.DoesNotExist:
            raise NotFound({"detail": "No User matches the given email."})

        membership = ProjectMembership.objects.filter(project=project, user=user).first()
        if not membership:
            return Response({"detail": "Membership not found."}, status=status.HTTP_404_NOT_FOUND)

        new_role = request.data.get('role')
        if not new_role:
            return Response({"detail": "Role is required."}, status=status.HTTP_400_BAD_REQUEST)

        membership.role = new_role
        membership.save()
        serializer = ProjectMembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='memberships/(?P<email>[^/.]+)/delete')
    def delete_membership_by_email(self, request, key=None, email=None):
        """
        Remove a user from the project.
        Only Admins or Project Owners can delete.
        """
        project, membership = self._get_project_membership_by_email(key, email)
        self._check_admin_or_owner(request.user, project)

        membership.delete()
        return Response({"detail": "Membership deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a project along with owner and memberships.
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
            "profile_image": owner.profile_image,
        }

        memberships_data = []
        for membership in project.memberships.all():
            member_user = membership.user
            memberships_data.append({
                "id": membership.id,
                "user": {
                    "id": member_user.id,
                    "username": member_user.username,
                    "first_name": member_user.first_name,
                    "last_name": member_user.last_name,
                    "email": member_user.email,
                    "profile_image": member_user.profile_image,
                },
                "role": membership.role,
                "joined_at": membership.joined_at,
            })

        project_data.update({
            'owner': owner_data,
            'memberships': memberships_data,
            'created_by': owner_data,
            'created_at': project.created_at,
            'type': project.type,
        })

        return Response(project_data)

    # ---------- Private Helper Methods ----------

    def _check_admin_or_owner(self, user, project):
        """
        Check if the user is Admin or Owner of the project.
        """
        if user == project.created_by:
            return
        membership = ProjectMembership.objects.filter(project=project, user=user).first()
        if not membership or membership.role != 'Admin':
            raise PermissionDenied(detail="Only Admins or the Project Owner can perform this action.")

    def _get_project_membership_by_email(self, key, email):
        """
        Helper to get project and membership object by project key and user email.
        """
        project = self.get_object()
        decoded_email = unquote(email)
        user = get_object_or_404(User, email=decoded_email)

        membership = ProjectMembership.objects.filter(project=project, user=user).first()
        if not membership:
            raise NotFound(detail="Membership not found.")

        return project, membership
