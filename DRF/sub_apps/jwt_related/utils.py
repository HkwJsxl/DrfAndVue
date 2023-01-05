"""自定义jwt认证"""

import jwt

from rest_framework_jwt.authentication import BaseAuthentication, BaseJSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler

from rest_framework import exceptions

from django.contrib.auth.models import User


class CustomCheck1(BaseAuthentication):
    def authenticate(self, request):
        jwt_value = request.META.get('HTTP_AUTHORIZATION')
        if not jwt_value:
            raise exceptions.AuthenticationFailed('没有携带jwt认证token.')
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('签名过期.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('用户非法.')
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))
        # payload就是用户信息的字典
        print(payload)
        # 需要得到user对象，
        # 第一种，去数据库查
        # user=User.objects.get(pk=payload.get('user_id'))
        # 第二种不查库
        user = User(pk=payload.get('user_id'), username=payload.get('username'))
        return user, jwt_value


class CustomCheck2(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        jwt_value = request.META.get('HTTP_AUTHORIZATION')
        if not jwt_value:
            raise exceptions.AuthenticationFailed('请携带要认证的签名.')
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('签名已过期.')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('签名解码错误.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('签名无效.')

        user_obj = User(pk=payload.get('user_id'), username=payload.get('username'))

        return user_obj, jwt_value
