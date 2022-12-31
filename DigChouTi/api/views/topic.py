from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.extension import mixins
from api import models
from api.seriazliers.account import LoginModelSerializer
from api.extension.exception_response import APIResponse
from api.extension import return_code
from api.seriazliers.topic import TopicModelSerializer
from api.extension.auth import TokenHeaderAuthentication


class TopicView(
    mixins.ReListModelMixin,
    mixins.ReCreateModelMixin,
    mixins.ReUpdateModelMixin,
    mixins.ReDestroyModelMixin,
    GenericViewSet
):
    authentication_classes = [TokenHeaderAuthentication, ]

    queryset = models.Topic.objects.filter(deleted=False).order_by('id')
    serializer_class = TopicModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
