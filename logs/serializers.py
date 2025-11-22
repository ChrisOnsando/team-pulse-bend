from typing import Any
from rest_framework import serializers
from logs.models import PulseLog, EventLog


class PulseLogSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)
    team_name = serializers.CharField(source="team.team_name", read_only=True)
    mood = serializers.IntegerField()
    workload = serializers.IntegerField()
    comment = serializers.CharField(allow_blank=True, required=False)
    team = serializers.UUIDField(required=False, allow_null=True)
    timestamp_local = serializers.DateTimeField(required=False, allow_null=True)
    year = serializers.IntegerField(required=False)
    week_index = serializers.IntegerField(required=False)
    
    class Meta:
        model = PulseLog
        fields = (
            "id",
            "user",
            "user_name",
            "mood",
            "workload",
            "comment",
            "timestamp",
            "team",
            "team_name",
            "timestamp_local",
            "year",
            "week_index",
            "created_at",
        )
        read_only_fields = ("id", "timestamp", "created_at")


class EventLogSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    event_name = serializers.CharField(max_length=255)
    metadata = serializers.CharField(allow_blank=True, required=False)
    
    class Meta:
        model = EventLog
        fields = ("id", "timestamp", "event_name", "metadata", "created_at")
        read_only_fields = ("id", "timestamp", "created_at")
        