from typing import Any
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from teams.models import Team
from teams.serializers import (
    TeamMemberSerializer,
    TeamSerializer,
    TeamUpdateSerializer,
)
from users.permissions import IsAdminUser

User = get_user_model()

class PublicTeamListView(generics.ListAPIView):
    """
    Public endpoint to list all teams (for signup page).
    No authentication required.
    """
    serializer_class = TeamSerializer
    permission_classes = (AllowAny,)
    queryset = Team.objects.all()
class TeamListCreateView(generics.ListCreateAPIView):
    """
    List all teams (authenticated users) or create a new team (admin only).
    """
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Team.objects.prefetch_related("members").all()
    
    def get_permissions(self):  # type: ignore[no-untyped-def]
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve (authenticated users), update or delete a team (admin only).
    """
    queryset = Team.objects.prefetch_related("members").all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_serializer_class(self):  # type: ignore[no-untyped-def]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return TeamUpdateSerializer
        return TeamSerializer
    
    def get_permissions(self):  # type: ignore[no-untyped-def]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class TeamAddMemberView(APIView):
    """
    Add a member to a team (admin only).
    """
    permission_classes = (IsAdminUser,)
    
    def post(self, request: Request, id: str) -> Response:
        team = get_object_or_404(Team, id=id)
        serializer = TeamMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data["user_id"]
        user = get_object_or_404(User, id=user_id)
        team.members.add(user)
        
        return Response(
            {"status": "member added"}, status=status.HTTP_200_OK
        )


class TeamRemoveMemberView(APIView):
    """
    Remove a member from a team (admin only).
    """
    permission_classes = (IsAdminUser,)
    
    def post(self, request: Request, id: str) -> Response:
        team = get_object_or_404(Team, id=id)
        serializer = TeamMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data["user_id"]
        user = get_object_or_404(User, id=user_id)
        team.members.remove(user)
        
        return Response(
            {"status": "member removed"}, status=status.HTTP_200_OK
        )
