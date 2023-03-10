from rest_framework.pagination import LimitOffsetPagination


class SelfLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    offset_query_param = None
