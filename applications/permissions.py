from rest_framework.permissions import BasePermission


class IsJobSeeker(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.role == 'job_seeker'
        return True