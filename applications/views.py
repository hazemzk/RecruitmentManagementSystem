from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Application
from .serializers import ApplicationSerializer
from users.models import ActivityLog


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # 🔒 AnonymousUser
        if not user or not user.is_authenticated:
            return Application.objects.none()

        # 👑 Admin
        if getattr(user, "role", None) == "admin":
            return Application.objects.all()

        # 🤝 Recruiter 
        if getattr(user, "role", None) == "recruiter":
            return Application.objects.filter(
                job__company__owner=user
            )

        # 👤 أي مستخدم عادي يشوف تطبيقاته فقط
        return Application.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required")

        application = serializer.save(user=user)

        ActivityLog.objects.create(
            user=user,
            action=f"Applied to job #{application.job.id}"
        )

    def update(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required")

        application = self.get_object()

        # 👑 Admin
        if getattr(user, "role", None) == "admin":
            response = super().update(request, *args, **kwargs)

            ActivityLog.objects.create(
                user=user,
                action=f"Admin updated application #{application.id}"
            )

            return response

        # 🤝 Recruiter
        if getattr(user, "role", None) == "recruiter":
            if application.job.company.owner != user:
                raise PermissionDenied("You cannot modify this application")

            response = super().update(request, *args, **kwargs)

            ActivityLog.objects.create(
                user=user,
                action=f"Updated status of application #{application.id}"
            )

            return response

        raise PermissionDenied("Only recruiters or admin can update status")
