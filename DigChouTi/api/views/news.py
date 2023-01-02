from rest_framework.viewsets import GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import filters, FilterSet

from api import models
from api.extension import mixins
from api.seriazliers.news import NewsModelSerializer
from api.extension.filter import SelfFilterBackend


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
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]
    filterset_class = NewsFilterSet

    queryset = models.News.objects.filter(deleted=False).order_by('-id')
    serializer_class = NewsModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
