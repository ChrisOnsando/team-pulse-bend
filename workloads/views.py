from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from workloads.models import Workload
from workloads.serializers import WorkloadSerializer
from users.permissions import IsAdminUser


class WorkloadListCreateView(generics.ListCreateAPIView):
    """
    List all workloads (authenticated users) or create a new workload (admin only).
    """
    queryset = Workload.objects.all()
    serializer_class = WorkloadSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_permissions(self):  # type: ignore[no-untyped-def]
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]


class WorkloadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve (authenticated users), update or delete a workload (admin only).
    """
    queryset = Workload.objects.all()
    serializer_class = WorkloadSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_permissions(self):  # type: ignore[no-untyped-def]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
