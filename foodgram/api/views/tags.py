from api.classesviewset import ListRetrieveViewSet
from rest_framework.permissions import AllowAny
from tags.models import Tag
from api.serializers.tags import TagSerializer


class TagsViewSet(ListRetrieveViewSet):
    """Работа с информацией о тэгах."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
