# DRF

## 常用

### 模块导入和语句

~~~python
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
# 版本控制
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning, AcceptHeaderVersioning, HostNameVersioning, NamespaceVersioning
# 反向生成url~~~~
request.versioning_scheme.reverse('视图别名', args=('v10',), request=request)
# 认证  # 认证的返回值后续可以在视图中使用(request.user, request.auth,)
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
# 权限
from rest_framework.permissions import BasePermission
~~~

### setting.py

~~~python
REST_FRAMEWORK = {
    "VERSION_PARAM": "version",  # 指定版本的key
    "DEFAULT_VERSION": "v1",  # 版本的默认值
    "ALLOWED_VERSIONS": ["v1", "v2", "v3"],  # 允许的版本号
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning"  # 全局配置
    
    # "UNAUTHENTICATED_USER": lambda: None,  # 认证返回值
    # "UNAUTHENTICATED_TOKEN": lambda: None,
    # "DEFAULT_AUTHENTICATION_CLASSES": ['utils.auth_related.TokenAuthentication', ]  # 全局配置
    # "DEFAULT_PERMISSION_CLASSES": ["utils.permission_related.RolePermission", ]
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
