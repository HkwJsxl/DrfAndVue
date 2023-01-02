from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import filters, FilterSet

from api import models
from api.seriazliers.recommend import RecommendModelSerializer
from api.extension import mixins
from api.extension.filter import SelfFilterBackend
from api.extension.exception_response import APIResponse


class RecommendFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = models.Recommend
        fields = ('latest_id',)


class RecommendView(
    mixins.ReListModelMixin,
    mixins.ReCreateModelMixin,
    mixins.ReDestroyModelMixin,
    GenericViewSet
):
    """收藏"""

    filter_backends = (SelfFilterBackend, DjangoFilterBackend)
    filterset_class = RecommendFilterSet

    queryset = models.Recommend.objects.all().order_by('-id')
    serializer_class = RecommendModelSerializer

    def perform_create(self, serializer):
        user = self.request.user
        instance = models.Recommend.objects.filter(user=user, **serializer.validated_data).first()
        if instance:
            # 已推荐的再次点击就是取消推荐
            instance.delete()
            instance.news.recommend_count -= 1
            instance.news.save()
            return APIResponse(message={'active': False})
        else:
            instance = models.Recommend.objects.create(user=user, **serializer.validated_data)
            instance.news.recommend_count += 1
            instance.news.save()
            return APIResponse(message={'active': True})
