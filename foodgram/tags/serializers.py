from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        model = Tag
        fields = '__all__'
