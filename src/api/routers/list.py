from rest_framework.routers import SimpleRouter

from api.views.list import ListViewSet


router = SimpleRouter(use_regex_path=False)


router.register("lists", ListViewSet)
