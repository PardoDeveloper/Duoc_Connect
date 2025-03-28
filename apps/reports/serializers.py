from rest_framework import serializers
from .models import AnonymousReport


class AnonymousReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousReport
        fields = ['id', 'category', 'description', 'submitted_at', 'is_reviewed']
        read_only_fields = ['submitted_at', 'is_reviewed']
