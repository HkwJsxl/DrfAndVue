from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api import models
from api.extension.exception_response import APIResponse
from api.extension import return_code


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            raise AuthenticationFailed(APIResponse(return_code.AUTH_FAILED, 'token认证失败'))
        user_obj = models.UserInfo.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed(APIResponse(return_code.AUTH_FAILED, 'token认证失败'))
        return user_obj, token

    def authenticate_header(self, request):
        return 'Bearer realm="API"'


class TokenHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed(APIResponse(return_code.AUTH_FAILED, 'token认证失败'))
        user_obj = models.UserInfo.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed(APIResponse(return_code.AUTH_FAILED, 'token认证失败'))
        return user_obj, token

    def authenticate_header(self, request):
        return 'Bearer realm="API"'
