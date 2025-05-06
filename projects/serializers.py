# serializers.py
from rest_framework import serializers
from accounts.models import User
from projects.models import Project, ProjectMembership


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_image']

    def get_profile_image(self, obj):
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return obj.profile_image.url
        return None


class ProjectMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = ProjectMembership
        fields = ['id', 'user', 'user_id', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class ProjectSerializer(serializers.ModelSerializer):
    memberships = ProjectMembershipSerializer(many=True, required=False)
    owner = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'key', 'image', 'type',
            'owner', 'memberships', 'created_by', 'created_at'
        ]
        read_only_fields = [
            'id', 'key', 'owner', 'memberships', 'created_by', 'created_at'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        memberships_data = self.initial_data.get('memberships', [])

        # Remove memberships from validated_data if somehow present
        validated_data.pop('memberships', None)

        project = Project.objects.create(
            owner=user,
            created_by=user,
            **validated_data
        )

        # Always add the creator as Admin if not manually added
        creator_included = any(
            int(m.get('user_id')) == user.id for m in memberships_data
        )
        if not creator_included:
            memberships_data.append({'user_id': user.id, 'role': 'Admin'})

        # Create memberships
        for membership in memberships_data:
            ProjectMembership.objects.create(
                project=project,
                user_id=membership['user_id'],
                role=membership['role']
            )

        return project

    def update(self, instance, validated_data):
        memberships_data = self.initial_data.get('memberships', [])

        validated_data.pop('memberships', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if memberships_data:
            for membership in memberships_data:
                ProjectMembership.objects.update_or_create(
                    project=instance,
                    user_id=membership['user_id'],
                    defaults={'role': membership['role']}
                )

        return instance
