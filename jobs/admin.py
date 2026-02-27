from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'salary', 'job_type', 'created_at')
    search_fields = ('title', 'company__name')
    list_filter = ('job_type', 'location')
    ordering = ('-created_at',)