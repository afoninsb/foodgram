from rest_framework import viewsets

from api.serializers.tags import TagSerializer
from tags.models import Tag


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с информацией о тэгах."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
