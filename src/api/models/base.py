from uuid import uuid4
from django.db import models
from django.utils import timezone

from api.managers.base import BaseManager


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]

    def delete(self, *args, **kwargs) -> None:
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs) -> None:
        super().delete(*args, **kwargs)
