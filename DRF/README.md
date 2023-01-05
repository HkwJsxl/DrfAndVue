# DRF

# 介绍

- sub_apps
  - 应用
  - version_manage：版本控制
  - auth_permission：认证和权限，utils/auth_related&permission_related
  - access_frequency：频率控制，utils/throttle_related
  - serializer_related：序列化
  - views_related：视图相关，utils/filter_related&page_related
  - exception_response：异常处理和自定义Response，utils/exception_response
  - practice：练习，practice
    ~~~
    图书一堆关联表的增删查改（APIView,GenericAPIView）
    ~~~
  - jwt_related：JWT，jwt_related
    ~~~
    1.控制jwt返回格式（utils/jwt_related）
    2.自定义基于jwt的认证（sub_apps/jwt_related/utils）
    3.多方式登录，自动签发
    
    使用jwt的JSONWebTokenAuthentication校验要加入一个权限控制
    from rest_framework_jwt.authentication import JSONWebTokenAuthentication
    from rest_framework.permissions import IsAuthenticated
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    JWT_AUTH = {
    # 控制jwt返回数据格式
      'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',
    }
    ~~~

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
    def parse_rate(self, rate):
        """重写：五分钟1次限制"""
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[-1]]
        count = int(period[0:-1])
        return num_requests, count * duration
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
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
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
"""异常处理和自定义Response"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
def re_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if not response:
        return APIResponse(1, 'errors: %s' % str(exc))
    return APIResponse(1, response.data.get('detail'))
class APIResponse(Response):
    def __init__(self, code=0, message='OK', data=None, *args, **kwargs):
        res_dict = {'code': code, 'message': message}
        if data:
            res_dict = {'code': code, 'message': message, 'data': data}
        res_dict.update(kwargs)
        super().__init__(data=res_dict, *args, **kwargs)
        
# 序列化类：self.context有三个值：request，format，view
# GenericAPIView源码
def get_serializer(self, *args, **kwargs):
    serializer_class = self.get_serializer_class()
    kwargs.setdefault('context', self.get_serializer_context())
    return serializer_class(*args, **kwargs)
def get_serializer_context(self):
    return {
        'request': self.request,
        'format': self.format_kwarg,
        'view': self
    }

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
    # 'PAGE_SIZE': 2,  # 分页
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

## 知识点

### Serializer高级用法

- source的使用

~~~
可以改字段名字：要展示的名字=serializers.CharField(source='数据库字段名')
可以.跨表：xxx=serializers.CharField(source='publish.email')
可以执行方法：xxx=serializers.CharField(source='test')  # test是表模型中的方法
~~~

- SerializerMethodField

~~~python
# 需要有个配套方法，get_字段名，返回值就是要显示的东西
from django.forms.models import model_to_dict
from rest_framework import serializers
roles = serializers.SerializerMethodField()
def get_roles(self, instance):
    role_queryset = instance.roles.all()
    return [model_to_dict(item, ['id', 'title']) for item in role_queryset]
~~~

### GenericAPIView的视图子类

~~~
（1）CreateAPIView
提供了post方法，内部调用了create方法
继承自： GenericAPIView、CreateModelMixin

（2）ListAPIView
提供了get方法，内部调用了list方法
继承自：GenericAPIView、ListModelMixin

（3）RetrieveAPIView
提供了get方法，内部调用了retrieve方法
继承自: GenericAPIView、RetrieveModelMixin

（4）DestroyAPIView
提供了delete方法，内部调用了Destroy方法
继承自：GenericAPIView、DestroyModelMixin

（5）UpdateAPIView
提供了put和patch方法，内部调用了update和partial_update方法
继承自：GenericAPIView、UpdateModelMixin

（6）ListCreateAPIView
提供了get和post方法，内部调用了list和create方法
继承自：GenericAPIView、ListModelMixin、CreateModelMixin

（7）RetrieveUpdateAPIView
提供 get、put、patch方法
继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin

（8）RetrieveDestroyAPIView
提供 get、delete方法
继承自：GenericAPIView、RetrieveModelMixin、DestroyModelMixin

（9）RetrieveUpdateDestroyAPIView
提供 get、put、patch、delete方法
继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestroyModelMixin
~~~

### routers

~~~python
from rest_framework import routers
# router = routers.DefaultRouter()
router = routers.SimpleRouter()
router.register(r'router', views.UserRouterModelView, basename='router')
urlpatterns = []
urlpatterns += router.urls
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

~~~
ModelSerializer反序列化的时候，设置read_only=True可以忽略传过来的字段，不写入到数据库。（不想让用户设置某个值）
从数据库读出来的数据，序列化返回出来的时候，不显示某个字段，可以设置write_only=True。（不想让用户看到某个值）
**两者不能同时设置**
~~~

### Serializer的many参数是如何根据传入不同布尔值生成不同的对象的

~~~python
"""
__new__方法是构建对象的，源码内部重写了__new__方法
"""
def __new__(cls, *args, **kwargs):
    if kwargs.pop('many', False):
        return cls.many_init(*args, **kwargs)
    return super().__new__(cls, *args, **kwargs)
~~~

### 序列化组件源码分析

~~~
序列化组件，先调用__new__方法，如果many=True，生成ListSerializer对象，如果为False，生成Serializer对象
序列化对象.data方法--调用父类data方法---调用对象自己的to_representation（自定义的序列化类无此方法，去父类找）
Aerializer类里有to_representation方法，for循环执行attribute = field.get_attribute(instance)
再去Field类里去找get_attribute方法，self.source_attrs就是被切分的source，然后执行get_attribute方法，source_attrs
当参数传过去，判断是方法就加括号执行，是属性就把值取出来
~~~



