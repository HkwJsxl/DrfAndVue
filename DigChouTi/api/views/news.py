from rest_framework.viewsets import GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import filters, FilterSet

from api import models
from api.extension import mixins
from api.seriazliers.news import NewsModelSerializer, IndexModelSerializer
from api.extension.filter import SelfFilterBackend
from api.extension.throttle import NewsRateThrottle
from api.extension.auth import UserAnonAuthentication


class NewsFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = models.News
        fields = ('latest_id',)


class NewsView(
    mixins.ReListModelMixin,
    mixins.ReCreateModelMixin,
    mixins.ReDestroyModelMixin,
    GenericViewSet
):
    """新闻资讯"""

    throttle_objects = [NewsRateThrottle(), ]
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]
    filterset_class = NewsFilterSet

    queryset = models.News.objects.filter(deleted=False).order_by('-id')
    serializer_class = NewsModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        # 数据插入成功后执行done方法，插入频率限制缓存记录
        for throttle in self.get_throttles():
            throttle.done()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

    def get_throttles(self):
        if self.request.method == 'POST':
            return self.throttle_objects
        return []


class IndexFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = models.News
        fields = ('latest_id', 'zone')


class IndexView(
    mixins.ReListModelMixin,
    GenericViewSet
):
    """首页"""
    authentication_classes = [UserAnonAuthentication, ]

    filter_backends = [DjangoFilterBackend]
    filterset_class = IndexFilterSet

    queryset = models.News.objects.filter(deleted=False, status=2).order_by('-id')
    serializer_class = IndexModelSerializer
