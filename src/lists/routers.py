from rest_framework.routers import SimpleRouter

from .views import ListViewSet, ActionViewSet


router = SimpleRouter(use_regex_path=False)


router.register("lists", ListViewSet)
router.register("lists/<uuid:list_id>/actions", ActionViewSet)
