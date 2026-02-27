from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active', 'created_at')
    list_filter = ('role', 'is_staff', 'is_active')

    ordering = ('-created_at',)
    search_fields = ('email', 'full_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone')}),
        ('Roles & Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Status', {'fields': ('is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )


admin.site.register(User, CustomUserAdmin)