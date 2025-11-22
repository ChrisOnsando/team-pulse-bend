from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from moods.models import Mood
from moods.serializers import MoodSerializer
from users.permissions import IsAdminUser


class MoodListCreateView(generics.ListCreateAPIView):
    """
    List all moods (authenticated users) or create a new mood (admin only).
    """
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_permissions(self):  # type: ignore[no-untyped-def]
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]


class MoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve (authenticated users), update or delete a mood (admin only).
    """
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_permissions(self):  # type: ignore[no-untyped-def]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
