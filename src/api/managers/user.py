from django.contrib.auth.models import UserManager as _UserManager

from api.managers.base import BaseManager


class UserManager(BaseManager, _UserManager):
    pass
