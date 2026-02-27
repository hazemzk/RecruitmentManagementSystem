from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)




from rest_framework.permissions import IsAdminUser
from django.db.models import Count
from companies.models import Company
from jobs.models import Job
from applications.models import Application
from .models import User, ActivityLog

class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        data = {
            "total_users": User.objects.count(),
            "total_companies": Company.objects.count(),
            "total_jobs": Job.objects.count(),
            "total_applications": Application.objects.count(),
            "accepted_applications": Application.objects.filter(status="accepted").count(),
            "rejected_applications": Application.objects.filter(status="rejected").count(),
        }

        return Response(data)

class ActivityLogView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logs = ActivityLog.objects.all().order_by("-created_at")
        data = [
            {
                "user": log.user.email,
                "action": log.action,
                "time": log.created_at
            }
            for log in logs
        ]

        return Response(data)