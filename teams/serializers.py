from typing import Any
from rest_framework import serializers
from teams.models import Team
from users.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    team_name = serializers.CharField(max_length=255)
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ("id", "team_name", "members", "member_count", "created_at")
        read_only_fields = ("id", "created_at")
    
    def get_member_count(self, obj: Any) -> int:
        return obj.members.count()


class TeamUpdateSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(max_length=255)
    
    class Meta:
        model = Team
        fields = ("team_name",)
    
    def update(self, instance: Any, validated_data: Any) -> Any:
        instance.team_name = validated_data.get("team_name", instance.team_name)
        instance.save()
        return instance


class TeamMemberSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    