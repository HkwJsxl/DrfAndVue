from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import filters, FilterSet

from api import models
from api.seriazliers.collect import CollectModelSerializer
from api.extension import mixins
from api.extension.filter import SelfFilterBackend
from api.extension.exception_response import APIResponse


class CollectFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = models.Collect
        fields = ('latest_id',)


class CollectView(
    mixins.ReListModelMixin,
    mixins.ReCreateModelMixin,
    mixins.ReDestroyModelMixin,
    GenericViewSet
):
    """收藏"""

    filter_backends = (SelfFilterBackend, DjangoFilterBackend)
    filterset_class = CollectFilterSet

    queryset = models.Collect.objects.all().order_by('-id')
    serializer_class = CollectModelSerializer

    def perform_create(self, serializer):
        user = self.request.user
        instance = models.Collect.objects.filter(user=user, **serializer.validated_data).first()
        if instance:
            # 已收藏的再次点击就是取消收藏
            instance.delete()
            instance.news.collect_count -= 1
            instance.news.save()
            return APIResponse(message={'active': False})
        else:
            instance = models.Collect.objects.create(user=user, **serializer.validated_data)
            instance.news.collect_count += 1
            instance.news.save()
            return APIResponse(message={'active': True})
