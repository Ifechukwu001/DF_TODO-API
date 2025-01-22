from django.contrib.auth.models import AbstractUser

from api.models.base import BaseModel
from api.managers.user import UserManager


class User(BaseModel, AbstractUser):
    email = None
    first_name = None
    last_name = None

    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta(BaseModel.Meta, AbstractUser.Meta):
        pass
