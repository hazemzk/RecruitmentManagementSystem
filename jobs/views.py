from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Job
from .serializers import JobSerializer
from .permissions import IsRecruiterOrReadOnly


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['job_type', 'location', 'company']
    search_fields = ['title', 'description']
    ordering_fields = ['salary', 'created_at']