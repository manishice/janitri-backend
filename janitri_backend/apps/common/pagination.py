from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil
from utils.responses import success_response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """
        Override default DRF paginated response to include page, total_pages
        and wrap it in success_response format.
        """
        page_number = self.page.number if self.page else 1
        page_size = self.get_page_size(self.request)
        total_items = self.page.paginator.count if self.page else len(data)
        total_pages = ceil(total_items / page_size) if page_size else 1

        paginated_data = {
            "count": total_items,
            "page": page_number,
            "page_size": page_size,
            "total_pages": total_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }

        # Wrap in success_response
        return success_response(message="Success", data=paginated_data)

