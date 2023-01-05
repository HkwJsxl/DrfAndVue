from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSet

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from sub_apps.jwt_related import ser
from utils.exception_response import APIResponse
from utils import return_code

"""自定义jwt校验"""
from sub_apps.jwt_related.utils import CustomCheck1
from sub_apps.jwt_related.utils import CustomCheck2


class UserRegView(ViewSet):
    def reg(self, request):
        serializer = ser.UserRegModelSerializer(data=request.data)
        if not serializer.is_valid():
            APIResponse(return_code.AUTH_FAILED, serializer.errors)
        return APIResponse(data=serializer.data)


class Test1APIView(APIView):
    # 需要登录（JSONWebTokenAuthentication + IsAuthenticated）
    # authentication_classes = [JSONWebTokenAuthentication, ]
    # 自定义jwt认证
    # authentication_classes = [CustomCheck1, ]
    authentication_classes = [CustomCheck2, ]
    # 权限控制
    permission_classes = [IsAuthenticated, ]
    """
    校验格式：
    请求头
    Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """

    def get(self, request, *args, **kwargs):
        return APIResponse(message='test1')


class Test2APIView(APIView):
    # 无需登录
    authentication_classes = [JSONWebTokenAuthentication, ]

    def get(self, request, *args, **kwargs):
        return APIResponse(message='test2')


class UserLoginView(ViewSet):
    authentication_classes = [CustomCheck2, ]
    permission_classes = []

    def login(self, request, *args, **kwargs):
        serializer = ser.UserLoginModelSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(return_code.AUTH_FAILED, serializer.errors)
        token = serializer.context.get('token')
        username = serializer.context.get('username')
        return APIResponse(message={'token': token, 'username': username})
