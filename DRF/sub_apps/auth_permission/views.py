import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import QueryParameterVersioning

from sub_apps.auth_permission import models
from utils.auth_related import TokenAuthentication
from utils.permission_related import RolePermission


class RegView(APIView):
    versioning_class = QueryParameterVersioning

    def post(self, request):
        current_version = request.version
        username = request.data.get('username')
        password = request.data.get('password')
        print(request.data)
        token = uuid.uuid1()
        models.UserInfo.objects.create(username=username, password=password, token=token)

        return Response({'status': 0, 'message': {'current_version': current_version, 'token': token}})


class LoginView(APIView):
    versioning_class = QueryParameterVersioning
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [RolePermission, ]

    def post(self, request):
        current_version = request.version

        username = request.data.get('username')
        password = request.data.get('password')
        token = request.auth
        user_obj = models.UserInfo.objects.filter(username=username, password=password, token=token)
        if not user_obj:
            return Response({'status': 0, 'message': {'current_version': current_version, 'auth': '用户名或密码错误,并检查token!'}})

        print(request.auth)  # 返回的token
        print(request.user)  # 用户对象
        return Response({'status': 0, 'message': {'current_version': current_version, 'auth': '登录成功!'}})


class OrderView(APIView):
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        if request.user:
            return Response({'status': 0, 'message': {'auth': '认证成功!', 'data': '人名币玩家!'}})
        return Response({'status': 0, 'message': {'auth': '认证失败!', 'data': '普通玩家!'}})


class AdminView(APIView):
    permission_classes = [RolePermission, ]

    def get(self, request):
        return Response({'status': 0, 'message': {'permission': '权限通过!'}})


