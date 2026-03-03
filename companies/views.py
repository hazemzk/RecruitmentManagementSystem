from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Company.objects.none()

        user = self.request.user

        if not user.is_authenticated:
            return Company.objects.none()

        if hasattr(user, "role") and user.role == "admin":
            return Company.objects.all()

        return Company.objects.filter(owner=user)

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, "role") or user.role != "recruiter":
            raise PermissionDenied("Only recruiters can create companies")

        serializer.save(owner=user)
