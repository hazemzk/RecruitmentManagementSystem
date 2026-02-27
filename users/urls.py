from django.contrib import admin
from django.urls import path
from .views import RegisterView, ProfileView, LogoutView, DashboardStatsView, ActivityLogView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )




admin.site.site_header = "Recruitment Management System"
admin.site.site_title = "RMS Admin"
admin.site.index_title = "Welcome to RMS Dashboard"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('activity-logs/', ActivityLogView.as_view(), name='activity-logs'),
]