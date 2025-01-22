from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone

from api.models import List, Action
from api.serializers import ActionMutateSerializer


@patch.object(ActionMutateSerializer, "context")
class TestActionMutateSerializer(TestCase):
    def setUp(self):
        self.list = List.objects.create(title="A new list")

    def test_deadline_is_not_required(self, mock_context):
        mock_context.get.return_value.kwargs.get.return_value = self.list.id
        serializer = ActionMutateSerializer(data={"description": "A new action"})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    @patch.object(List, "objects")
    def test_deadline_is_valid_isoformat(
        self,
        mock_list_objects,
        mock_context,
    ):
        mock_list_objects.get.return_value.created_at = self.list.created_at
        mock_context.get.return_value.kwargs.get.return_value = self.list.id

        serializer = ActionMutateSerializer(
            data={
                "description": "A new action",
                "deadline": self.list.created_at.isoformat(),
            }
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        serializer = ActionMutateSerializer(
            data={"description": "A new action", "deadline": "2021_01_03"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ["deadline"])

    @patch.object(List, "objects")
    def test_deadline_is_passed_list_created_date(
        self,
        mock_list_objects,
        mock_context,
    ):
        mock_list_objects.get.return_value.created_at = self.list.created_at
        mock_context.get.return_value.kwargs.get.return_value = self.list.id

        serializer = ActionMutateSerializer(
            data={"description": "A new action", "deadline": self.list.created_at}
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        action = Action.objects.create(list=self.list, description="An action")
        serializer = ActionMutateSerializer(
            action,
            data={
                "deadline": self.list.created_at - timezone.timedelta(days=1),
            },
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ["deadline"])

        serializer = ActionMutateSerializer(
            data={
                "description": "A new action",
                "deadline": self.list.created_at - timezone.timedelta(days=1),
            },
        )

        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ["deadline"])
