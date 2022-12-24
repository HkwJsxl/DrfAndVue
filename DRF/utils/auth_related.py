from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from auth_permission import models


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        current_version = request.version
        token = request.query_params.get('token')
        if not token:
            raise AuthenticationFailed({'status': 0, 'message': {'current_version': current_version, 'auth': 'token认证失败!'}})
        user_obj = models.UserInfo.objects.filter(token=token)
        if not user_obj:
            raise AuthenticationFailed({'status': 0, 'message': {'current_version': current_version, 'auth': 'token认证失败!'}})
        return user_obj, token

    def authenticate_header(self, request):
        return 'Bearer realm="API"'
