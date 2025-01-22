from rest_framework import serializers
from api.models import List

from .action import ActionListSerializer


class ListBaseSerializer(serializers.ModelSerializer):
    actions = ActionListSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ["id", "title", "note"]


class ListMutateSerializer(ListBaseSerializer):
    class Meta(ListBaseSerializer.Meta):
        fields = ["id", "title", "note"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        return super().create(validated_data)


class ListSerializer(ListBaseSerializer):
    class Meta:
        model = List
        fields = ["id", "title", "note", "actions", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
