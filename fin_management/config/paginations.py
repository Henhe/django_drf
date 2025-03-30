from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "per_page"

    def get_paginated_response(self, data):
        response = {
            "data": data,
            "meta": {
                "count": self.page.paginator.count,
                "page": int(self.request.query_params.get(self.page_query_param, 1)),
                "per_page": int(self.request.query_params.get(self.page_size_query_param, self.page_size)),
            }
        }
        return Response(response)