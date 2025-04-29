from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'key'  # Assuming 'key' is the unique identifier for tasks

    def get_queryset(self):
        """
        Restrict tasks to the given project based on the project key in the URL.
        """
        queryset = self.queryset
        project_key = self.kwargs['project_key']  # Get the project_key from the URL
        
        # Filter tasks by the project_key
        queryset = queryset.filter(project__key=project_key)

        # Additional filters based on query parameters
        name = self.request.query_params.get('name')
        search = self.request.query_params.get('search')
        task_status = self.request.query_params.get('status')
        task_priority = self.request.query_params.get('priority')
        task_assigned_me = self.request.query_params.get('assigned_to')

        if name:
            queryset = queryset.filter(title__icontains=name)
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

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a task by its unique key.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new task.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing task.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a task by its unique key.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
