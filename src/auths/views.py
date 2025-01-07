from dj_rest_auth.views import LoginView as DJLoginView, LogoutView as DJLogoutView
from dj_rest_auth.registration.views import RegisterView as DJRegisterView
from drf_spectacular.utils import extend_schema


class RegisterAPIView(DJRegisterView):
    pass


class LoginAPIView(DJLoginView):
    pass


class LogoutAPIView(DJLogoutView):
    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(request=None, responses=None)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
