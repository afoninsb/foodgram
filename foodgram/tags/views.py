from foodgram.classesviewset import ListRetrieveViewSet
from tags.serializers import TagSerializer
from tags.models import Tag


class TagsViewSet(ListRetrieveViewSet):
    """Работа с информацией о тэгах."""

    queryset = Tag.objects.all()
    lookup_field = 'id'
    serializer_class = TagSerializer
