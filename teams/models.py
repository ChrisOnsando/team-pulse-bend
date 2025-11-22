import uuid
from django.conf import settings
from django.db import models
from app.abstracts import TimeStampedModel


class Team(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    team_name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        blank=True,
    )
    
    class Meta:
        db_table = "teams"
    
    def __str__(self) -> str:
        return self.team_name
