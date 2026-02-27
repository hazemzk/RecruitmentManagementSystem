from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'salary',
            'location',
            'job_type',
            'company',
            'company_name',
            'created_at'
        ]
        read_only_fields = ['created_at']