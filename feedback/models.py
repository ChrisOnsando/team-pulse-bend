import uuid
from django.conf import settings
from django.db import models
from app.abstracts import TimeStampedModel


class TeamFeedback(TimeStampedModel):
    """
    Team Feedback Model
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_feedbacks",
        help_text="User who gave the feedback"
    )
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="feedbacks",
        help_text="Team the feedback is for"
    )
    message = models.TextField()
    is_anonymous = models.BooleanField(
        default=False,
        help_text="Whether to hide the user's identity"
    )
    
    class Meta:
        db_table = "team_feedbacks"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["team", "is_anonymous"]),
        ]
    
    def __str__(self) -> str:
        return f"Feedback by {self.user.username} for {self.team.team_name}"
