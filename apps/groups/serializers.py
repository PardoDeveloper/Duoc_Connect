from rest_framework import serializers
from .models import StudyGroup, GroupMembership


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
