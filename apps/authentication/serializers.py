from rest_framework import serializers
from .models import CustomUser, SecurityLog


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        if not value.endswith('@duocuc.cl'):
            raise serializers.ValidationError("El correo debe ser institucional (@duocuc.cl)")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class ProfilePhotoSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()

class SecurityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityLog
        fields = ['user', 'action', 'timestamp']