from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
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
    lookup_field = 'key' # Assuming 'key' is the unique identifier for tasks

    def get_queryset(self):
        """
        Optionally restricts the returned tasks to a given project,
        by filtering against a `project` query parameter in the URL.
        """
        queryset = self.queryset
        project_key = self.request.query_params.get('project')
        if project_key:
            queryset = queryset.filter(project__key=project_key)

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
    
    