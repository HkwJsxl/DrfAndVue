from rest_framework.filters import BaseFilterBackend
from django_filters import FilterSet, filters

from sub_apps.views_related import models


# 自定义筛选类
class CustomFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user_id = request.query_params.get('pk')
        if not user_id:
            return queryset
        return queryset.filter(pk=user_id)


class UserFilterSet(FilterSet):
    gte_id = filters.NumberFilter(field_name='id', lookup_expr='gte')
    age = filters.NumberFilter(field_name='age', lookup_expr='gte')

    class Meta:
        model = models.UserInfo
        fields = ["gte_id", "age"]


class UserFilterSet2(FilterSet):
    gte_id = filters.NumberFilter(field_name='id', lookup_expr='gte')
    name = filters.CharFilter(field_name="username", lookup_expr="exact", exclude=True)
    # depart = filters.CharFilter(field_name="depart__title", lookup_expr="contains")
    # token = filters.BooleanFilter(field_name="token", lookup_expr="isnull")
    email = filters.CharFilter(field_name="email", lookup_expr="startswith")

    # /api/users/?level=2&level=1   -> "level" = 1 OR "level" = 2（必须的是存在的数据，否则报错-->内部有校验机制）
    # level = filters.AllValuesMultipleFilter(field_name="level", lookup_expr="exact")
    level = filters.MultipleChoiceFilter(field_name="level", lookup_expr="exact", choices=models.UserInfo.level_choices)
    # ?age=18,20     -> age in [18,20]
    age = filters.BaseInFilter(field_name='age', lookup_expr="in")
    # ?range_id_max=10&range_id_min=1    -> id BETWEEN 1 AND 10
    range_id = filters.NumericRangeFilter(field_name='id', lookup_expr='range')

    # ?ordering=id     -> order by id asc
    # ?ordering=-id     -> order by id desc
    # ?ordering=age     -> order by age asc
    # ?ordering=-age     -> order by age desc
    ordering = filters.OrderingFilter(fields=["id", "age"])

    # ?size=1     -> limit 1（自定义搜索）
    size = filters.CharFilter(method='filter_size', distinct=False, required=False)

    class Meta:
        model = models.UserInfo
        fields = ["id", "gte_id", "name", "email", "level", "age", 'range_id', "size", "ordering"]

    def filter_size(self, queryset, name, value):
        int_value = int(value)
        return queryset[0:int_value]
