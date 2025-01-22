from dj_rest_auth.views import LogoutView as DJLogoutView
from drf_spectacular.utils import extend_schema


class LogoutAPIView(DJLogoutView):
    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(request=None, responses=None)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
