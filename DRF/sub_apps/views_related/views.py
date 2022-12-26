from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.viewsets import ViewSet, ViewSetMixin
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from sub_apps.views_related import models
from sub_apps.views_related import ser_view
from utils.permission_related import IDPermission


class UserModelView(ModelViewSet):
    permission_classes = [IDPermission, ]

    # ModelViewSet包括所有的增删改查ModelMixin
    queryset = models.UserInfo.objects.all()
    serializer_class = ser_view.UserModelSerializer

    # 重写功能方法
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 0, 'message': {'data': serializer.data}})

    def perform_create(self, serializer):
        serializer.save(password='123456', email="create@create.com")  # 不校验的字段要自己传值

    def perform_update(self, serializer):
        serializer.save(password='666', email='new@new.com')  # 不校验的字段要自己传值
