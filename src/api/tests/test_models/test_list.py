from django.test import TestCase

from api.models import List


class TestList(TestCase):
    def test_str(self):
        list_obj = List.objects.create(title="A new list")
        self.assertEqual(str(list_obj), "A new list")
