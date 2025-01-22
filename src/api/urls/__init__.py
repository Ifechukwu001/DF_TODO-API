from django.urls import path, include

from .auth import auth_urls
from .v1 import v1_urls


urlpatterns = [
    path("v1/", include([*auth_urls, *v1_urls])),
]
