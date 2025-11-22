from django.contrib import admin
from moods.models import Mood


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ["value", "description", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["description"]
    ordering = ["value"]
