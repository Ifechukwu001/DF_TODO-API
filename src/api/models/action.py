from django.db import models


from api.models.base import BaseModel


class Action(BaseModel):
    list = models.ForeignKey(
        "api.List", on_delete=models.CASCADE, related_name="actions"
    )
    description = models.CharField(max_length=100)
    deadline = models.DateTimeField(blank=True, null=True)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.id.hex
