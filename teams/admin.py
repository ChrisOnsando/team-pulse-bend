from django.contrib import admin
from teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["team_name", "member_count", "created_at"]
    search_fields = ["team_name"]
    filter_horizontal = ["members"]
    ordering = ["-created_at"]
    
    def member_count(self, obj) -> int:
        return obj.members.count()
    
    member_count.short_description = "Members"
