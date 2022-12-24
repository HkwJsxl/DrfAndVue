import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import QueryParameterVersioning
from rest_framework.authentication import BaseAuthentication

from auth_permission import models
from utils.auth_related import TokenAuthentication


class RegView(APIView):
    versioning_class = QueryParameterVersioning

    def post(self, request):
        current_version = request.version
        username = request.data.get('username')
        password = request.data.get('password')
        print(request.data)
        token = uuid.uuid1()
        user_obj = models.UserInfo.objects.create(username=username, password=password, token=token)

        return Response({'status': 0, 'message': {'current_version': current_version, 'token': token}})


class LoginView(APIView):
    versioning_class = QueryParameterVersioning
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        current_version = request.version

        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = models.UserInfo.objects.filter(username=username, password=password)
        if not user_obj:
            return Response({'status': 0, 'message': {'current_version': current_version, 'auth': '用户名或密码错误!'}})

        print(request.auth)  # 返回的token
        print(request.user)  # 用户对象
        return Response({'status': 0, 'message': {'current_version': current_version, 'auth': '登录成功!'}})


class OrderView(APIView):
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        if request.user:
            return Response({'status': 0, 'message': {'auth': '认证成功!', 'data': '人名币玩家!'}})
        return Response({'status': 0, 'message': {'auth': '认证失败!', 'data': '普通玩家!'}})
