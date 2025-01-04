from rest_framework.routers import SimpleRouter

from .views import ListViewSet


router = SimpleRouter()


router.register("lists", ListViewSet)
