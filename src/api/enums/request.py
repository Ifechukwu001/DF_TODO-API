from enum import StrEnum


class RequestAction(StrEnum):
    CREATE = "create"
    RETRIEVE = "retrieve"
    LIST = "list"
    DESTROY = "destroy"
