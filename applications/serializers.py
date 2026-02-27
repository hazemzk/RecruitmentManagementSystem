from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = Application
        fields = [
            'id',
            'user',
            'user_email',
            'job',
            'job_title',
            'cv',
            'status',
            'applied_at'
        ]
        read_only_fields = ['status', 'applied_at', 'user']