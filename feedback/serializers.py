from typing import Any
from rest_framework import serializers
from feedback.models import TeamFeedback
from teams.models import Team

class TeamFeedbackSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.SerializerMethodField()
    message = serializers.CharField()
    is_anonymous = serializers.BooleanField(default=False)
    team = serializers.UUIDField(write_only=True, required=False)  
    team_name = serializers.CharField(source="team.team_name", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = TeamFeedback
        fields = (
            "id",
            "username",
            "message",
            "is_anonymous",
            "team",
            "team_name",
            "created_at",
        )
        read_only_fields = ("id", "username", "team_name", "created_at")
    
    def get_username(self, obj: Any) -> str:
        """
        Return 'Anonymous' if feedback is anonymous, otherwise return username
        """
        if obj.is_anonymous:
            return "Anonymous"
        return obj.user.username
    
    def create(self, validated_data: Any) -> Any:
        user = self.context["request"].user
        
        if user.is_staff:
            team_id = validated_data.pop("team", None)
            
            if not team_id:
                raise serializers.ValidationError(
                    {"team": "Admin users must specify a team"}
                )
            
            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                raise serializers.ValidationError(
                    {"team": "Team not found"}
                )
            
            validated_data["team"] = team
        else:
            user_teams = user.teams.all()
            
            if not user_teams.exists():
                raise serializers.ValidationError(
                    {"error": "You must belong to a team to submit feedback"}
                )
            
            validated_data["team"] = user_teams.first()
        
        validated_data["user"] = user
        
        return super().create(validated_data)
    