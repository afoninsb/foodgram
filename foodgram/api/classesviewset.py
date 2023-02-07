from rest_framework import mixins, viewsets


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet POST-запросов для создания новых объектов."""


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet GET-запросов для получения списка объектов."""


class CreateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet POST-запросов для создания новых объектов и
    GET-запросов для получения списка и одиночных объектов.
    """
