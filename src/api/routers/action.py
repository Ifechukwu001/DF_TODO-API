from rest_framework.routers import SimpleRouter

from api.views.action import ActionViewSet


router = SimpleRouter(use_regex_path=False)


router.register("lists/<uuid:list_id>/actions", ActionViewSet)
