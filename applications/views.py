from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.db.models import Q

from .models import Application
from .serializers import ApplicationSerializer
from users.models import ActivityLog


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Application.objects.all()

        if user.role == "recruiter":

            return Application.objects.filter(
                job__company__owner=user
            )

        return Application.objects.filter(user=user)

    def perform_create(self, serializer):
        application = serializer.save(user=self.request.user)

        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Applied to job #{application.job.id}"
        )

    def update(self, request, *args, **kwargs):
        user = request.user
        application = self.get_object()

        if user.role == "admin":
            response = super().update(request, *args, **kwargs)

            ActivityLog.objects.create(
                user=user,
                action=f"Admin updated application #{application.id}"
            )

            return response

        if user.role == "recruiter":
            if application.job.company.owner != user:
                raise PermissionDenied("You cannot modify this application")

            response = super().update(request, *args, **kwargs)

            ActivityLog.objects.create(
                user=user,
                action=f"Updated status of application #{application.id}"
            )

            return response

        raise PermissionDenied("Only recruiters or admin can update status")