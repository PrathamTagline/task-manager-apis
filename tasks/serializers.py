from rest_framework import serializers
from .models import Task, TaskComment, SubTask, TaskIssue
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SubTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for subtasks.
    """
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'key', 'status', 'created_at']


class TaskCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for task comments.
    """
    user = UserSerializer()

    class Meta:
        model = TaskComment
        fields = ['id', 'user', 'content', 'created_at']


class TaskIssueSerializer(serializers.ModelSerializer):
    """
    Serializer for task issues.
    """
    user = UserSerializer()

    class Meta:
        model = TaskIssue
        fields = ['id', 'user', 'content', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks with nested relationships.
    """
    assigned_to = UserSerializer()
    assigned_by = UserSerializer()
    created_by = UserSerializer()
    subtasks = SubTaskSerializer(many=True)
    comments = TaskCommentSerializer(many=True)
    issues = TaskIssueSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'key', 'description',
            'assigned_to', 'assigned_by', 'created_by',
            'priority', 'status', 'due_date', 'start_time', 'end_time',
            'estimated_duration', 'actual_duration',
            'subtasks', 'comments', 'issues', 'created_at'
        ]