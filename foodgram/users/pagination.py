from rest_framework.pagination import PageNumberPagination, Response


class UserPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'response': data
        })
