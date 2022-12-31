import uuid
import datetime

from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import GenericAPIView

from api.seriazliers.account import RegModelSerializer, LoginModelSerializer
from api.extension.mixins import ReCreateModelMixin
from api import models
from api.seriazliers.account import LoginModelSerializer
from api.extension.exception_response import APIResponse
from api.extension import return_code


class RegView(ReCreateModelMixin, GenericViewSet):
    """注册"""
    authentication_classes = []
    permission_classes = []
    serializer_class = RegModelSerializer

    def perform_create(self, serializer):
        # 数据库中没有confirm_password字段
        serializer.validated_data.pop('confirm_password')
        serializer.save()


class LoginView(APIView):
    """登录"""
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginModelSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(return_code.VALIDATE_ERROR, serializer.errors)

        username = request.data.get('username')
        phone = request.data.get('phone')
        password = request.data.get('password')

        obj = models.UserInfo.objects.filter(
            Q(Q(username=username) | Q(phone=phone), password=password), deleted=False
        ).first()

        if not obj:
            return APIResponse(return_code.AUTH_FAILED, '用户名或密码错误!')

        token = uuid.uuid4()
        obj.token = token
        obj.token_expiry_date = datetime.datetime.now() + datetime.timedelta(weeks=2)
        obj.save()
        return APIResponse(message={'username': obj.username, 'token': obj.token})
