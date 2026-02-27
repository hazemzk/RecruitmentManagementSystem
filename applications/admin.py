from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at')
    search_fields = ('user__email', 'job__title')
    list_filter = ('status',)
    ordering = ('-applied_at',)