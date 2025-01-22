from django.db import models
from django.conf import settings

from api.models.base import BaseModel


class List(BaseModel):
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lists",
        null=True,
    )

    def __str__(self) -> str:
        return self.title
