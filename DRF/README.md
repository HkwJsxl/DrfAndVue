# DRF

## 常用

### 模块导入和语句

~~~python
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
"""版本控制"""
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning, AcceptHeaderVersioning, HostNameVersioning, NamespaceVersioning
"""反向生成url"""
request.versioning_scheme.reverse('视图别名', args=('v10',), request=request)
"""认证  # 认证的返回值后续可以在视图中使用(request.user, request.auth,)"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
"""权限"""
from rest_framework.permissions import BasePermission
"""访问频率限制"""
from rest_framework.throttling import SimpleRateThrottle
from rest_framework import exceptions
from rest_framework import status
from django.core.cache import cache as default_cache
class ThrottledException(exceptions.APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 'throttled'
class RateThrottle(SimpleRateThrottle):
    cache = default_cache  # 访问记录存放在django的缓存中（需设置缓存）
    scope = 'user_access'  # 构造缓存中的key
    # 设置访问频率, 's', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day'
    THROTTLE_RATES = {scope: '10/m'}
    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk  # 用户ID
        else:
            ident = self.get_ident(request)  # 获取请求用户IP（去request中找请求头）
        return self.cache_format % {'scope': self.scope, 'ident': ident}
    def throttle_failure(self):
        wait = self.wait()
        detail = {
            'status': 1005,
            'message': '访问频率限制',
            'detail': '需等待{}s才能访问'.format(int(wait))
        }
        raise ThrottledException(detail)
~~~

### setting.py

~~~python
# LANGUAGE_CODE = "zh-hans"  # 语言更改为汉字（数据校验错误信息...）

REST_FRAMEWORK = {
    "VERSION_PARAM": "version",  # 指定版本的key
    "DEFAULT_VERSION": "v1",  # 版本的默认值
    "ALLOWED_VERSIONS": ["v1", "v2", "v3"],  # 允许的版本号
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning"  # 全局配置
    
    # "UNAUTHENTICATED_USER": lambda: None,  # 认证返回值
    # "UNAUTHENTICATED_TOKEN": lambda: None,
    # "DEFAULT_AUTHENTICATION_CLASSES": ['utils.auth_related.TokenAuthentication', ]  # 全局配置
    # "DEFAULT_PERMISSION_CLASSES": ["utils.permission_related.RolePermission", ]
    
    # "DEFAULT_THROTTLE_CLASSES": ["utils.throttle_related.RateThrottle", ],  # 全局配置
    # "DEFAULT_THROTTLE_RATES": {
    #     "user_access": "10/m",
    # }
}

"""缓存"""
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "123456",
        }
    }
}
~~~

## 问题

### DRF在使用request时如何实现不用点击method从而获取里面的属性

~~~python
from rest_framework.request import Request

class Request:
    def __getattr__(self, attr):
        try:
            return getattr(self._request, attr)
        except AttributeError:
            return self.__getattribute__(attr)
~~~
