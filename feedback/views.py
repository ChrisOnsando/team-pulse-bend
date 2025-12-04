from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from feedback.models import TeamFeedback
from feedback.serializers import TeamFeedbackSerializer


class TeamFeedbackListCreateView(generics.ListCreateAPIView):
    """
    List team feedbacks or create new feedback.
    - Authenticated users can create feedback
    - Message is required
    - User and team are automatically assigned from logged-in user
    """
    serializer_class = TeamFeedbackSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["is_anonymous", "team"]
    ordering_fields = ["created_at"]
    
    def get_queryset(self):  # type: ignore[no-untyped-def]
        user = self.request.user
        
        if user.is_staff:
            return TeamFeedback.objects.select_related("user", "team").all()
        
        user_teams = user.teams.all()
        return TeamFeedback.objects.filter(
            team__in=user_teams
        ).select_related("user", "team")


class TeamFeedbackDetailView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a team feedback.
    - Users can only delete their own feedback
    - Admins can delete any feedback
    """
    serializer_class = TeamFeedbackSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_queryset(self):  # type: ignore[no-untyped-def]
        user = self.request.user
        
        if user.is_staff:
            return TeamFeedback.objects.select_related("user", "team").all()
        
        return TeamFeedback.objects.filter(user=user).select_related("user", "team")
