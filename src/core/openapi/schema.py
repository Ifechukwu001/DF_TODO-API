from drf_spectacular.openapi import AutoSchema
from rest_framework.permissions import IsAuthenticated

from .serializers import ErrorResponseSerializer
from .utils import enveloper


class EnvelopeAutoSchema(AutoSchema):
    def get_response_serializers(self):
        # Get the base serializer for the success response
        base_serializer = super().get_response_serializers()

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
        enveloped_serializer = enveloper(
            base_serializer.__class__,
            self._is_list_view(serializer=base_serializer),
        )

        return {
            200: enveloped_serializer,
            **error_responses,
        }
