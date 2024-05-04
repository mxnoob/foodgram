from rest_framework.pagination import PageNumberPagination


class FoodgramPagination(PageNumberPagination):
    """Пагинация для проекта"""

    page_size = 6
    page_size_query_param = 'limit'
