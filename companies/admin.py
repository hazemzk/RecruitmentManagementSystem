from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'created_at')
    search_fields = ('name', 'location', 'owner__email')
    list_filter = ('location', 'created_at')
    ordering = ('-created_at',)

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "description", "location", "website")
        }),
        ("Owner", {
            "fields": ("owner",)
        }),
    )