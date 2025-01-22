from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_paths = [path("", include("api.urls"))]

urlpatterns = [
    path(
        "api/",
        include(
            api_paths,
        ),
    ),
    path("admin/", admin.site.urls),
    # Redirect to Swagger Docs
    path("", RedirectView.as_view(url="api/docs/")),
    # Swagger Docs
    path("api/schema/", SpectacularJSONAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
