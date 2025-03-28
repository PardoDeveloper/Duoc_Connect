from rest_framework import serializers
from .models import StudyGroup, GroupMembership, SharedFile


class StudyGroupSerializer(serializers.ModelSerializer):
    creator_email = serializers.EmailField(source='creator.email', read_only=True)

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'description', 'creator_email', 'created_at', 'is_private']


class GroupMembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'group', 'user_email', 'joined_at']

class SharedFileSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)

    class Meta:
        model = SharedFile
        fields = ['id', 'group', 'file', 'description', 'uploaded_by_email', 'uploaded_at']