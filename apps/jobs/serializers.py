from rest_framework import serializers
from .models import JobOffer, JobApplication


class JobOfferSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta:
        model = JobOffer
        fields = ['id', 'title', 'description', 'company', 'location', 'created_at', 'created_by_email']


class JobApplicationSerializer(serializers.ModelSerializer):
    applicant_email = serializers.EmailField(source='applicant.email', read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'job_offer', 'cover_letter', 'applicant_email', 'applied_at']
