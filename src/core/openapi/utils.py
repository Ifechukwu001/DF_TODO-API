import functools
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer


@functools.cache
def enveloper(serializer_class: serializers.Serializer, many: bool):
    component_name = "{}{}Response".format(
        serializer_class.__name__.replace("Serializer", ""),
        "Array" if many else "",
    )

    @extend_schema_serializer(many=False, component_name=component_name)
    class EnvelopeSerializer(serializers.Serializer):
        status = serializers.BooleanField()
        message = serializers.CharField()
        data = serializer_class(many=many)

    return EnvelopeSerializer
