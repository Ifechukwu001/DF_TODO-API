from dj_rest_auth.serializers import TokenSerializer
from drf_spectacular.openapi import AutoSchema
from rest_framework.permissions import IsAuthenticated

from api.enums.request import RequestAction
from .serializers import ErrorResponseSerializer
from .utils import enveloper


class EnvelopeAutoSchema(AutoSchema):
    def get_response_serializers(self):
        # Get the base serializer for the success response
        base_serializer = super().get_response_serializers()
        success_response = dict()

        if getattr(self.view, "action", False):
            if base_serializer is None:
                enveloped_serializer = None
            else:
                enveloped_serializer = enveloper(
                    base_serializer.__class__,
                    self._is_list_view(serializer=base_serializer),
                )

            if self.view.action == RequestAction.CREATE:
                success_response.update(
                    {
                        201: enveloped_serializer,
                    }
                )
            elif self.view.action == RequestAction.DESTROY:
                success_response.update(
                    {
                        204: None,
                    }
                )
            else:
                success_response.update(
                    {
                        200: enveloped_serializer,
                    }
                )

        else:
            from api.views.auth import RegisterAPIView

            if base_serializer is None:
                enveloped_serializer = None
            else:
                enveloped_serializer = enveloper(
                    TokenSerializer,
                    False,
                )

            if isinstance(self.view, RegisterAPIView):
                success_response.update(
                    {
                        201: enveloped_serializer,
                    }
                )
            else:
                success_response.update(
                    {
                        200: enveloped_serializer,
                    }
                )

        # Base error responses applicable to all endpoints
        error_responses = {
            400: ErrorResponseSerializer,
            404: ErrorResponseSerializer,
        }

        # Add authentication-related error codes if the endpoint requires authentication
        if IsAuthenticated in [perm.__class__ for perm in self.view.permission_classes]:
            error_responses.update(
                {
                    401: ErrorResponseSerializer,
                    403: ErrorResponseSerializer,
                }
            )

        # Combine success and error responses
        return {
            **success_response,
            **error_responses,
        }
