from rest_framework.filters import BaseFilterBackend


class SelfFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # 筛选出来的都是当前用户的
        return queryset.filter(user=request.user)
