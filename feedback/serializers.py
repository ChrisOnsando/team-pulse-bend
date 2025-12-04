from typing import Any
from rest_framework import serializers
from feedback.models import TeamFeedback


class TeamFeedbackSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.SerializerMethodField()
    message = serializers.CharField()
    is_anonymous = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = TeamFeedback
        fields = (
            "id",
            "username",
            "message",
            "is_anonymous",
            "created_at",
        )
        read_only_fields = ("id", "username", "created_at")
    
    def get_username(self, obj: Any) -> str:
        """
        Return 'Anonymous' if feedback is anonymous, otherwise return username
        """
        if obj.is_anonymous:
            return "Anonymous"
        return obj.user.username
    
    def create(self, validated_data: Any) -> Any:
        user = self.context["request"].user
        
        user_teams = user.teams.all()
        
        if not user_teams.exists():
            raise serializers.ValidationError(
                {"error": "You must belong to a team to submit feedback"}
            )
        
        validated_data["user"] = user
        validated_data["team"] = user_teams.first()
        
        return super().create(validated_data)
    