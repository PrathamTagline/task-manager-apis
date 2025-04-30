from rest_framework import serializers

from projects.models import Project
from .models import Task, TaskComment, SubTask, TaskIssue
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TaskSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for tasks with nested relationships.
    """
    assigned_to = UserSerializer()
    assigned_by = UserSerializer()
    created_by = UserSerializer()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'key', 'description',
            'assigned_to', 'assigned_by', 'created_by',
            'priority', 'status', 'due_date', 'start_time', 'end_time',
            'estimated_duration', 'actual_duration',
            'created_at'
        ]


class TaskWriteSerializer(serializers.ModelSerializer):
    """
    Write-only serializer for creating/updating tasks.
    Assigns task using user's email instead of ID.
    """
    assigned_to = serializers.EmailField(write_only=True)
    project_key = serializers.CharField(write_only=True)

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'priority', 'status',
            'due_date', 'start_time', 'end_time',
            'estimated_duration', 'actual_duration', 'assigned_to', 'project_key'
        ]

    def validate_assigned_to(self, value):
        try:
            user = User.objects.get(email=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email.")

    def validate_project_key(self, value):
        try:
            project = Project.objects.get(key=value)
            return project
        except Project.DoesNotExist:
            raise serializers.ValidationError(
                f"Project with key '{value}' does not exist.")

    def create(self, validated_data):
        request = self.context['request']
        assigned_to = validated_data.pop('assigned_to')
        project = validated_data.pop('project_key')  # Get the project
        validated_data['assigned_to'] = assigned_to
        validated_data['assigned_by'] = request.user
        validated_data['created_by'] = request.user
        validated_data['project'] = project  # Assign the project

        task = Task.objects.create(**validated_data)

        return task
    def update(self, instance, validated_data):
        assigned_to = validated_data.pop('assigned_to', None)
        if assigned_to:
            instance.assigned_to = assigned_to
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance