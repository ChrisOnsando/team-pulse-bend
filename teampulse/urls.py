from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (
    LogoutView,
    UserDetailView,
    UserListView,
    UserMeView,
    UserRegisterView,
)
from teams.views import (
    TeamAddMemberView,
    TeamDetailView,
    TeamListCreateView,
    TeamRemoveMemberView,
)
from moods.views import MoodDetailView, MoodListCreateView
from workloads.views import WorkloadDetailView, WorkloadListCreateView
from logs.views import (
    EventLogDetailView,
    EventLogListCreateView,
    PulseLogDetailView,
    PulseLogListCreateView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Authentication endpoints
    path("api/v1/auth/register/", UserRegisterView.as_view(), name="user-register"),
    path("api/v1/auth/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/v1/auth/logout/", LogoutView.as_view(), name="user-logout"),
    
    # User endpoints
    path("api/v1/users/", UserListView.as_view(), name="user-list"),
    path("api/v1/users/me/", UserMeView.as_view(), name="user-me"),
    path("api/v1/users/<uuid:id>/", UserDetailView.as_view(), name="user-detail"),
    
    # Team endpoints
    path("api/v1/teams/", TeamListCreateView.as_view(), name="team-list-create"),
    path("api/v1/teams/<uuid:id>/", TeamDetailView.as_view(), name="team-detail"),
    path("api/v1/teams/<uuid:id>/add-member/", TeamAddMemberView.as_view(), name="team-add-member"),
    path("api/v1/teams/<uuid:id>/remove-member/", TeamRemoveMemberView.as_view(), name="team-remove-member"),
    
    # Mood endpoints
    path("api/v1/moods/", MoodListCreateView.as_view(), name="mood-list-create"),
    path("api/v1/moods/<uuid:id>/", MoodDetailView.as_view(), name="mood-detail"),
    
    # Workload endpoints
    path("api/v1/workloads/", WorkloadListCreateView.as_view(), name="workload-list-create"),
    path("api/v1/workloads/<uuid:id>/", WorkloadDetailView.as_view(), name="workload-detail"),
    
    # Pulse log endpoints
    path("api/v1/pulse-logs/", PulseLogListCreateView.as_view(), name="pulselog-list-create"),
    path("api/v1/pulse-logs/<uuid:id>/", PulseLogDetailView.as_view(), name="pulselog-detail"),
    
    # Event log endpoints
    path("api/v1/event-logs/", EventLogListCreateView.as_view(), name="eventlog-list-create"),
    path("api/v1/event-logs/<uuid:id>/", EventLogDetailView.as_view(), name="eventlog-detail"),
]
