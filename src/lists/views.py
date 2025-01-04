from rest_framework import viewsets

from .models import List, Action
from .serializers import ListSerializer, ActionSerializer


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    queryset = List.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]


class ActionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
