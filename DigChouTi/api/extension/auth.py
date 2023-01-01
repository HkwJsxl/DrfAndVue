import datetime

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api import models
from api.extension import return_code


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            raise AuthenticationFailed({'code': return_code.AUTH_FAILED, 'errors': '认证失败!'})
        user_obj = models.UserInfo.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed({'code': return_code.AUTH_FAILED, 'errors': '认证失败!'})
        # token过期
        if datetime.datetime.now() > user_obj.token_expiry_date:
            raise AuthenticationFailed({'code': return_code.AUTH_OVERDUE, 'errors': '认证已过期!'})
        return user_obj, token

    def authenticate_header(self, request):
        return 'Bearer realm="API"'


class TokenHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed({'code': return_code.AUTH_FAILED, 'errors': '认证失败!'})
        user_obj = models.UserInfo.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed({'code': return_code.AUTH_FAILED, 'errors': '认证失败!'})
        # token过期
        if datetime.datetime.now() > user_obj.token_expiry_date:
            raise AuthenticationFailed({'code': return_code.AUTH_OVERDUE, 'errors': '认证已过期!'})
        return user_obj, token

    def authenticate_header(self, request):
        return 'Bearer realm="API"'
