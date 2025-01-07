from rest_framework import serializers
from lists.models import List


from auths.utils import get_session_id
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
        session = get_session_id(self.context["request"])
        if user.is_authenticated:
            validated_data["user"] = user
        else:
            validated_data["session"] = session

        return super().create(validated_data)


class ListSerializer(ListBaseSerializer):
    class Meta:
        model = List
        fields = ["id", "title", "note", "actions", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
