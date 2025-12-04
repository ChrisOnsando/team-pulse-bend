from django.contrib import admin
from feedback.models import TeamFeedback


@admin.register(TeamFeedback)
class TeamFeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "get_author_display",
        "team",
        "is_anonymous",
        "message_preview",
        "created_at",
    ]
    list_filter = ["is_anonymous", "team", "created_at"]
    search_fields = ["message", "user__username", "team__team_name"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    
    def get_author_display(self, obj):  # type: ignore[no-untyped-def]
        if obj.is_anonymous:
            return "Anonymous"
        return obj.user.username
    
    get_author_display.short_description = "Author"
    
    def message_preview(self, obj):  # type: ignore[no-untyped-def]
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    
    message_preview.short_description = "Message"
