from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        # /service/authors/ -> authors
        type = self.request.path.split("/")[2]
        return Response(
            {
                "type": type,
                "items": data,
            }
        )
