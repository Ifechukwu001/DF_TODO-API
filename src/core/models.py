from django.db import models
from django.utils import timezone


class BaseManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().exclude(deleted=True)


class BaseModel(models.Model):
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
