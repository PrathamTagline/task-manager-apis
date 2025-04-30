from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from projects.models import Project
from .models import Task
from .serializers import TaskSerializer, TaskWriteSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'key'

    def get_serializer_class(self):
        """
        Use write serializer for create/update, and read serializer for retrieve/list.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return TaskWriteSerializer
        return TaskSerializer

    def get_queryset(self):
        """
        Restrict tasks to the given project based on the project key in the URL.
        """
        queryset = self.queryset
        project_key = self.kwargs.get('project_key')
        if project_key:
            queryset = queryset.filter(project__key=project_key)

        # Optional filters
        title = self.request.query_params.get('title')
        search = self.request.query_params.get('search')
        task_status = self.request.query_params.get('status')
        task_priority = self.request.query_params.get('priority')
        task_assigned_me = self.request.query_params.get('assigned_to')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if search:
            queryset = queryset.filter(title__icontains=search)
        if task_status:
            queryset = queryset.filter(status__iexact=task_status)
        if task_priority:
            queryset = queryset.filter(priority__iexact=task_priority)

        if task_assigned_me:
            queryset = queryset.filter(assigned_to=self.request.user)
        else:
            queryset = queryset.filter(assigned_to__isnull=False)

        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Create a new task, automatically associating it with the project
        retrieved from the project_key in the URL.
        """
        project_key = kwargs.get('project_key')  # Get project_key from URL

        # Retrieve the project based on the project_key
        try:
            project = Project.objects.get(key=project_key)
        except Project.DoesNotExist:
            raise ValidationError(f"Project with key '{project_key}' does not exist.")

        # Now add the project to the task data before saving
        task_data = request.data.copy()  # Make a copy to modify
        task_data['project_key'] = project.key  # Add the project_key to the data

        # Proceed with normal task creation
        serializer = self.get_serializer(data=task_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Update a task by its unique key.
        """
        Project_key = kwargs.get('project_key')
        try:
            project = Project.objects.get(key=Project_key)
        except Project.DoesNotExist:
            raise ValidationError(f"Project with key '{Project_key}' does not exist.")
        task_data = request.data.copy()
        task_data['project_key'] = project.key
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=task_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)    

    def destroy(self, request, *args, **kwargs):
        """
        Delete a task by its unique key.
        """
        project_key = kwargs.get('project_key')
        try:
            project = Project.objects.get(key=project_key)
        except Project.DoesNotExist:
            raise ValidationError(f"Project with key '{project_key}' does not exist.")
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

