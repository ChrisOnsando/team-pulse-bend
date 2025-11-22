import uuid
from django.db import models
from app.abstracts import TimeStampedModel


class Workload(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    value = models.IntegerField(unique=True)
    description = models.CharField(max_length=255)
    image_url = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = "workloads"
        ordering = ["value"]
    
    def __str__(self) -> str:
        return f"{self.value} - {self.description}"
