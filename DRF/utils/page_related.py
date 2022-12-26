from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination


class UserPageNumberPagination(PageNumberPagination):
    page_size = 2  # 每页数量
    page_query_param = 'size'  # ?size=xxx
    max_page_size = 100  # 最大可访问页


class UserCursorPagination(CursorPagination):
    ordering = 'id'
    page_size = 2  # 每页数量
    page_query_param = 'size'  # ?size=xxx
    max_page_size = 100  # 最大可访问页


class UserModelPageNumberPagination(PageNumberPagination):
    page_size = 2  # 每页数量
    page_query_param = 'size'  # ?size=xxx
    max_page_size = 100  # 最大可访问页


class UserModelLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2  # 每页数量
    max_limit = 3


class UserModelCursorPagination(CursorPagination):
    ordering = 'id'
    page_size = 2  # 每页数量
    page_query_param = 'size'  # ?size=xxx
    max_page_size = 100  # 最大可访问页
