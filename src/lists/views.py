from rest_framework import generics, viewsets, mixins, response, status
from drf_spectacular.utils import extend_schema

from auths.utils import get_session_id
from .models import List, Action
from .serializers import (
    ListSerializer,
    ListMutateSerializer,
    ActionSerializer,
    ActionMutateSerializer,
    ActionListSerializer,
)


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListMutateSerializer
    queryset = List.objects.all()
    lookup_field = "id"
    lookup_value_converter = "uuid"
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return self.queryset.filter(session=get_session_id(self.request))

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ListSerializer
        return super().get_serializer_class()


class ActionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ActionMutateSerializer
    queryset = Action.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActionSerializer
        if self.action == "list":
            return ActionListSerializer
        return super().get_serializer_class()

    def validate_list_id(self, list_id):
        queryset = List.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        else:
            queryset = queryset.filter(session=get_session_id(self.request))

        generics.get_object_or_404(queryset, id=list_id)

    def update_queryset(self, list_id):
        self.validate_list_id(list_id)
        self.queryset = self.queryset.filter(list_id=list_id)

    @extend_schema(
        request=ActionMutateSerializer,
        responses=ActionSerializer,
    )
    def create(self, request, *args, **kwargs):
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
        self.update_queryset(kwargs["list_id"])
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses=ActionListSerializer,
    )
    def list(self, request, *args, **kwargs):
        self.update_queryset(kwargs["list_id"])
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=ActionMutateSerializer,
        responses=ActionSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        self.update_queryset(kwargs["list_id"])
        action = self.get_object()
        serializer = self.get_serializer(action, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        action = serializer.save()
        return response.Response(ActionSerializer(action).data)

    def delete(self, request, *args, **kwargs):
        self.update_queryset(kwargs["list_id"])
        return super().destroy(request, *args, **kwargs)
