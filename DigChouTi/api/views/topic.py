from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

from api.extension import mixins
from api import models
from api.seriazliers.topic import TopicModelSerializer
# from api.extension.auth import TokenHeaderAuthentication
# from api.extension.exception_response import APIResponse
# from api.extension import return_code
from api.extension.filter import SelfFilterBackend


class SelfFilterSet(FilterSet):
    # ?latest_id=99             ->  id<=99
    # ?latest_id=99&limit=10    ->  id<=99  limit 10
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = models.Topic
        fields = ('latest_id', )


class TopicView(
    mixins.ReListModelMixin,
    mixins.ReCreateModelMixin,
    mixins.ReUpdateModelMixin,
    mixins.ReDestroyModelMixin,
    GenericViewSet
):
    filter_backends = [SelfFilterBackend, DjangoFilterBackend]
    filterset_class = SelfFilterSet

    queryset = models.Topic.objects.filter(deleted=False).order_by('id')
    serializer_class = TopicModelSerializer

    def perform_create(self, serializer):
        # 主题是由当前用户创建的
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
