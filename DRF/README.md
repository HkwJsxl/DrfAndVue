# DRF

## 常用

### 模块导入和语句

~~~python
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
"""状态码"""
from rest_framework import status
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
"""钩子错误信息"""
from rest_framework.exceptions import ValidationError
"""视图"""
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.viewsets import ViewSet, ViewSetMixin
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
"""筛选"""
from rest_framework.filters import BaseFilterBackend
from django_filters import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
"""分页"""
from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination
"""解析器"""
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
"""路由"""
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'router', views.UserRouterModelView)
~~~

### setting.py

~~~python
#把英文改为中文
LANGUAGE_CODE = 'zh-hans'
#把国际时区改为中国时区
TIME_ZONE = 'Asia/Shanghai'

REST_FRAMEWORK = {
    "VERSION_PARAM": "version",  # 指定版本的key
    "DEFAULT_VERSION": "v1",  # 版本的默认值
    "ALLOWED_VERSIONS": ["v1", "v2", "v3"],  # 允许的版本号
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning"  # 全局配置
    
    # "UNAUTHENTICATED_USER": lambda: None,  # 认证返回值
    # "UNAUTHENTICATED_TOKEN": lambda: None,
    # "DEFAULT_AUTHENTICATION_CLASSES": ['utils.auth_related.TokenAuthentication', ]  # 认证
    # "DEFAULT_PERMISSION_CLASSES": ["utils.permission_related.RolePermission", ]  # 权限
    
    # "DEFAULT_THROTTLE_CLASSES": ["utils.throttle_related.RateThrottle", ],  # 频率限制
    # "DEFAULT_THROTTLE_RATES": {
    #     "user_access": "10/m",
    # }
    
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend', ]  # 筛选
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

### read_only,write_only区别

~~~python
ModelSerializer反序列化的时候，设置read_only=True可以忽略传过来的字段，不写入到数据库。（不想让用户设置某个值）
从数据库读出来的数据，序列化返回出来的时候，不显示某个字段，可以设置write_only=True。（不想让用户看到某个值）
**两者不能同时设置**
~~~
