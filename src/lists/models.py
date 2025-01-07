from django.db import models
from django.conf import settings
from core.models import BaseModel


class List(BaseModel):
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)

    # User Identification
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lists",
        null=True,
    )
    session = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.title


class Action(BaseModel):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="actions")
    description = models.CharField(max_length=100)
    deadline = models.DateTimeField(blank=True, null=True)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.id.hex
