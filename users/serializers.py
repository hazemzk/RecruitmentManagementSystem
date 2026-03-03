from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'phone',
            'role',
            'created_at'
        ]

       read_only_fields = ['id', 'email', 'role', 'created_at']
