# serializers.py
from rest_framework import serializers
from accounts.models import User
from projects.models import Project, ProjectMembership

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ProjectMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ['id', 'user', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at']

class ProjectSerializer(serializers.ModelSerializer):
    memberships = ProjectMembershipSerializer(many=True, required=False)  # memberships can be optional
    owner = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)  # Added created_by
    created_at = serializers.DateTimeField(read_only=True)  # Added created_at

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'key', 'image','type', 'owner', 'memberships', 'created_by', 'created_at']
        read_only_fields = ['id', 'key', 'owner', 'memberships', 'created_by', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user who is creating the project
        memberships_data = self.initial_data.get('memberships', [])
        
        # Create the project
        project = Project.objects.create(owner=user, **validated_data)

        # If memberships data is provided, create ProjectMemberships for the project
        # Add creator as 'Admin' if they are not part of the memberships
        if not any(m['user'] == user.id for m in memberships_data):
            memberships_data.append({'user': user.id, 'role': 'Admin'})
        
        # Create memberships for the project
        for membership_data in memberships_data:
            ProjectMembership.objects.create(project=project, **membership_data)

        return project

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        # Handle the case where memberships might be updated (e.g., adding/removing members)
        memberships_data = validated_data.get('memberships', None)
        if memberships_data is not None:
            # Update memberships
            for membership_data in memberships_data:
                user = membership_data['user']
                role = membership_data['role']
                # Assuming we have a way to update the existing memberships
                ProjectMembership.objects.update_or_create(
                    project=instance, user=user, defaults={'role': role}
                )
        
        return instance
