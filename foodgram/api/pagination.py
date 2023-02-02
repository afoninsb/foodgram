from django.conf import settings
from rest_framework.pagination import PageNumberPagination, Response


class RecipePagination(PageNumberPagination):
    """Пагинатор для вывода списка рецептов."""

    page_size = settings.RECIPE_PER_PAGE
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
