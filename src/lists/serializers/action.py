from rest_framework import serializers
from lists.models import List, Action


class ActionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "description", "deadline", "done"]


class ActionMutateSerializer(ActionBaseSerializer):
    class Meta(ActionBaseSerializer.Meta):
        fields = ["description", "deadline"]
        allow_null = ["deadline"]

    def validate_deadline(self, deadline):
        if deadline:
            if self.instance and deadline < self.instance.list.created_at:
                raise serializers.ValidationError(
                    "Deadline cannot be before list creation date."
                )
            elif not self.instance:
                list_id = self.context.get("view").kwargs.get("list_id")
                list = List.objects.get(id=list_id)
                if deadline < list.created_at:
                    raise serializers.ValidationError(
                        "Deadline cannot be before list creation date."
                    )
        return deadline

    def validate(self, data):
        data["list_id"] = self.context.get("view").kwargs.get("list_id")
        return data


class ActionSerializer(ActionBaseSerializer):
    class Meta(ActionBaseSerializer.Meta):
        fields = ["id", "description", "deadline", "done", "created_at", "updated_at"]


class ActionListSerializer(ActionBaseSerializer):
    pass
