from rest_framework.pagination import PageNumberPagination, Response


class UserPagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'response': data,
        })
