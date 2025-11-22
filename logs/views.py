from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from logs.models import PulseLog, EventLog
from logs.serializers import EventLogSerializer, PulseLogSerializer
from users.permissions import IsAdminUser


class PulseLogListCreateView(generics.ListCreateAPIView):
    """
    List and create pulse logs. 
    - Authenticated users can view their own logs and create logs
    - Admins can view all logs
    """
    serializer_class = PulseLogSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["user", "team", "year", "week_index", "mood", "workload"]
    ordering_fields = ["timestamp", "year", "week_index"]
    
    def get_queryset(self):  # type: ignore[no-untyped-def]
        user = self.request.user
        if user.is_staff:
            return PulseLog.objects.select_related("user", "team").all()
        return PulseLog.objects.filter(user=user).select_related("user", "team")


class PulseLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a pulse log.
    - Users can only access their own logs
    - Admins can access all logs
    """
    serializer_class = PulseLogSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_queryset(self):  # type: ignore[no-untyped-def]
        user = self.request.user
        if user.is_staff:
            return PulseLog.objects.select_related("user", "team").all()
        return PulseLog.objects.filter(user=user).select_related("user", "team")


class EventLogListCreateView(generics.ListCreateAPIView):
    """
    List event logs or create a new event log (admin only).
    """
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["event_name"]
    ordering_fields = ["timestamp"]


class EventLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an event log (admin only).
    """
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"
