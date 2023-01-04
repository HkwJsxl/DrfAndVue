from rest_framework.viewsets import GenericViewSet

from app01 import models
from app01 import serializer
from extension.mixins import ReCreateModelMixin, ReUpdateModelMixin, ReRetrieveModelMixin
from app01.throttle import IPThrottle


class UserCreateGenericViewSet(ReCreateModelMixin, ReRetrieveModelMixin, ReUpdateModelMixin, GenericViewSet):
    """
    用户注册，
    用户中心，
    更新头像
    """
    throttle_objects = [IPThrottle(), ]

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

    def get_throttles(self):
        """测试：自定义频率限制"""
        if self.action == 'retrieve':
            return self.throttle_objects
        return []
