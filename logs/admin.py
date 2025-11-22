from django.contrib import admin
from logs.models import EventLog, PulseLog


@admin.register(PulseLog)
class PulseLogAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "mood",
        "workload",
        "team",
        "year",
        "week_index",
        "timestamp",
    ]
    list_filter = ["mood", "workload", "team", "year", "week_index", "timestamp"]
    search_fields = ["user__username", "user__email", "comment"]
    ordering = ["-timestamp"]
    readonly_fields = ["timestamp", "created_at", "updated_at"]
    
    def get_queryset(self, request):  # type: ignore[no-untyped-def]
        return super().get_queryset(request).select_related("user", "team")


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ["event_name", "timestamp", "created_at"]
    list_filter = ["event_name", "timestamp"]
    search_fields = ["event_name", "metadata"]
    ordering = ["-timestamp"]
    readonly_fields = ["timestamp", "created_at", "updated_at"]
