from django.urls import path

from api.views.auth import RegisterAPIView, LoginAPIView, LogoutAPIView


auth_urls = [
    path("auth/register/", RegisterAPIView.as_view(), name="auth_register"),
    path("auth/login/", LoginAPIView.as_view(), name="auth_login"),
    path("auth/logout/", LogoutAPIView.as_view(), name="auth_logout"),
]
