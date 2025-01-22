from django.urls import path, include

from api.routers.list import router as list_router
from api.routers.action import router as action_router

v1_urls = [
    path("", include(list_router.urls)),
    path("", include(action_router.urls)),
]
