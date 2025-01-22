from rest_framework import (
    generics,
    viewsets,
    filters,
    mixins,
    serializers,
    response,
    status,
)
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from api.models import List, Action
from api.serializers import (
    ActionSerializer,
    ActionMutateSerializer,
    ActionListSerializer,
)
from api.enums.request import RequestAction


class ActionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ActionMutateSerializer
    queryset = Action.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["description"]

    def get_serializer_class(self):
        if self.action == RequestAction.RETRIEVE:
            return ActionSerializer
        if self.action == RequestAction.LIST:
            return ActionListSerializer
        return super().get_serializer_class()

    def validate_list_id(self, list_id):
        queryset = List.objects.filter(user=self.request.user)
        generics.get_object_or_404(queryset, id=list_id)

    def update_queryset(self, list_id):
        self.validate_list_id(list_id)
        self.queryset = self.queryset.filter(list_id=list_id)

    @extend_schema(
        request=ActionMutateSerializer,
        responses=ActionSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Creates a new action on a list of the authenticated user
        """
        self.validate_list_id(kwargs["list_id"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.save()
        return response.Response(
            ActionSerializer(action).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses=ActionSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves an action on a list of the authenticated user
        """
        self.update_queryset(kwargs["list_id"])
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses=ActionListSerializer,
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieves all actions on a list of the authenticated user
        """

        self.update_queryset(kwargs["list_id"])
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=ActionMutateSerializer,
        responses=ActionSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Updates the action on a list of the authenticated user
        """

        self.update_queryset(kwargs["list_id"])
        action = self.get_object()
        serializer = self.get_serializer(action, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        action = serializer.save()
        return response.Response(ActionSerializer(action).data)

    @extend_schema(
        request=None,
        responses=ActionSerializer,
    )
    @action(detail=True, methods=["post"])
    def mark_done(self, *args, **kwargs):
        """
        Marks an action as done
        """
        self.update_queryset(kwargs["list_id"])
        action = self.get_object()
        if action.done:
            raise serializers.ValidationError("Action already done")
        action.done = True
        action.save()
        return response.Response(ActionSerializer(action).data)

    @extend_schema(
        request=None,
        responses=ActionSerializer,
    )
    @action(detail=True, methods=["post"])
    def mark_undone(self, *args, **kwargs):
        """
        Marks an action as undone
        """
        self.update_queryset(kwargs["list_id"])
        action = self.get_object()
        if not action.done:
            raise serializers.ValidationError("Action is not done")
        action.done = False
        action.save()
        return response.Response(ActionSerializer(action).data)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes the action of the authenticated user
        """
        self.update_queryset(kwargs["list_id"])
        return super().destroy(request, *args, **kwargs)
