from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data, type=None):
        """
        Returns a paginated response that matches the required format.
        "type" is the name of the list of items in the response.
        """
        if not type:
            # /service/authors/ -> authors
            type = self.request.path.split("/")[2]
        return Response(
            {
                "type": type,
                "items": data,
            }
        )


# Returns a pagination class with output like:
# {
#  "type": "label",
#  "items": [...]
# }
def labelled_pagination(label: str):
    class Pagination(pagination.PageNumberPagination):
        def get_paginated_response(self, data):
            return Response(
                {
                    "type": label,
                    "items": data,
                }
            )

    return Pagination
