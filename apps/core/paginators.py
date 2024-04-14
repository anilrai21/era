from rest_framework.pagination import PageNumberPagination

from .constants import PAGINATION_NUMBER


class EraPagination(PageNumberPagination):
    page_size = PAGINATION_NUMBER
