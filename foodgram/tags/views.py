from rest_framework.permissions import AllowAny

from foodgram.classesviewset import ListRetrieveViewSet
from tags.models import Tag
from tags.serializers import TagSerializer


class TagsViewSet(ListRetrieveViewSet):
    """Работа с информацией о тэгах."""

    queryset = Tag.objects.all()
    lookup_field = 'id'
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
