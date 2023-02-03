from rest_framework.permissions import AllowAny

from api.classesviewset import ListRetrieveViewSet
from api.serializers.tags import TagSerializer
from tags.models import Tag


class TagsViewSet(ListRetrieveViewSet):
    """Работа с информацией о тэгах."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
