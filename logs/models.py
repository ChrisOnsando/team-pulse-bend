import uuid
from datetime import datetime
from django.conf import settings
from django.db import models
from app.abstracts import TimeStampedModel


class PulseLog(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pulse_logs",
    )
    mood = models.IntegerField()
    workload = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pulse_logs",
    )
    timestamp_local = models.DateTimeField(null=True, blank=True)
    year = models.IntegerField()
    week_index = models.IntegerField()
    
    class Meta:
        db_table = "pulse_logs"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
            models.Index(fields=["user", "year", "week_index"]),
        ]
    
    def save(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        if not self.year or not self.week_index:
            now = datetime.now()
            self.year = now.year
            self.week_index = now.isocalendar()[1]
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.user.username} - Week {self.week_index}, {self.year}"


class EventLog(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    event_name = models.CharField(max_length=255)
    metadata = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = "event_logs"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
            models.Index(fields=["event_name"]),
        ]
    
    def __str__(self) -> str:
        return f"{self.event_name} - {self.timestamp}"
