from typing import Any
from rest_framework import serializers
from feedback.models import TeamFeedback
from teams.models import Team


class TeamFeedbackSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    username = serializers.SerializerMethodField()
    message = serializers.CharField()
    is_anonymous = serializers.BooleanField(default=False)
    team = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    team_name = serializers.SerializerMethodField()
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

    def get_team_name(self, obj: Any) -> str:
        """
        Return team name or 'General' if no team
        """
        if obj.team:
            return obj.team.team_name
        return "General"

    def create(self, validated_data: Any) -> Any:
        user = self.context["request"].user
        team_id = validated_data.pop("team", None)

        if user.is_staff:
            if team_id:
                try:
                    validated_data["team"] = Team.objects.get(id=team_id)
                except Team.DoesNotExist:
                    raise serializers.ValidationError(
                        {"team": "Team not found"}
                    )
            else:
                validated_data["team"] = None
        else:
            user_teams = user.teams.all()
            if not user_teams.exists():
                raise serializers.ValidationError(
                    {"error": "You must belong to a team to submit feedback"}
                )
            
            if team_id:
                try:
                    team = Team.objects.get(id=team_id)
                    if team not in user_teams:
                        raise serializers.ValidationError(
                            {"team": "You are not a member of this team"}
                        )
                    validated_data["team"] = team
                except Team.DoesNotExist:
                    raise serializers.ValidationError(
                        {"team": "Team not found"}
                    )
            else:
                validated_data["team"] = user_teams.first()

        validated_data["user"] = user
        return super().create(validated_data)
