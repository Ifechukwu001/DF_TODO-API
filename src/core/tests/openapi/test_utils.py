from django.test import SimpleTestCase
from rest_framework import serializers

from core.openapi.utils import enveloper


class Serializer(serializers.Serializer):
    """Test Serializer"""

    field = serializers.CharField(help_text="Field description.")


class TestEnveloper(SimpleTestCase):
    def test_enveloper(self):
        enveloped1 = enveloper(Serializer, many=False)
        enveloped2 = enveloper(Serializer, many=False)
        self.assertEqual(enveloped1, enveloped2)
