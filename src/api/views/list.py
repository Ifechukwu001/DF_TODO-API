from rest_framework import (
    viewsets,
    filters,
)

from api.models import List
from api.serializers import (
    ListSerializer,
    ListMutateSerializer,
)
from api.enums.request import RequestAction


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListMutateSerializer
    queryset = List.objects.all()
    lookup_field = "id"
    lookup_value_converter = "uuid"
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == RequestAction.RETRIEVE:
            return ListSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves the list of the authenticated user
        """
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Retrieves all lists of the authenticated user
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Creates a new list for the authenticated user
        """
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Updates the list of the authenticated user
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes the list of the authenticated user
        """
        return super().destroy(request, *args, **kwargs)
