from rest_framework.viewsets import GenericViewSet

from app01 import models
from app01 import serializer
from extension.mixins import ReCreateModelMixin, ReUpdateModelMixin, ReRetrieveModelMixin


class UserCreateGenericViewSet(ReCreateModelMixin, ReRetrieveModelMixin, ReUpdateModelMixin, GenericViewSet):
    """
    用户注册，
    用户中心，
    更新头像
    """
    queryset = models.UserInfo.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            # 用户注册
            return serializer.UserCreateModelSerializer
        elif self.action == 'retrieve':
            # 用户中心
            return serializer.UserRetrieveModelSerializer
        elif self.action == 'update':
            # 更新头像
            return serializer.UserUpdateModelSerializer
        else:
            return []
