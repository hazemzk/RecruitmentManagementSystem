from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer
from .permissions import IsRecruiter


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        
        if user.role == 'admin':
            return Company.objects.all()

      
        return Company.objects.filter(owner=user)

    def perform_create(self, serializer):
        if self.request.user.role != 'recruiter':
            raise PermissionError("Only recruiters can create companies")

        serializer.save(owner=self.request.user)