from django.test import TestCase

from api.models import List, Action


class TestAction(TestCase):
    def setUp(self):
        self.list_obj = List.objects.create(title="A new list")

    def test_str(self):
        action = Action.objects.create(description="A new action", list=self.list_obj)
        self.assertEqual(str(action), action.id.hex)
