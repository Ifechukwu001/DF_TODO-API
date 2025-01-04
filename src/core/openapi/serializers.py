from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    """Base Error response serializer"""

    status = serializers.BooleanField(
        default=False, help_text="Status of the response."
    )
    message = serializers.CharField(help_text="Error message describing the issue.")
    errors = serializers.SerializerMethodField(
        required=False, help_text="Optional field with detailed errors."
    )

    def get_errors(self, instance) -> list[str]:
        return []
