from django.urls import path, include, re_path
from sub_apps.jwt_related import views

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt import settings

from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    # 注册
    path('user/reg/', views.UserRegView.as_view({'post': 'reg'})),
    # 登录
    path('user/login/', obtain_jwt_token),
    # 测试是否登录能进入
    path('test1/', views.Test1APIView.as_view()),
    path('test2/', views.Test2APIView.as_view()),
    # 多方式登录
    path('user/login2/', views.UserLoginView.as_view({'post': 'login'})),
]

urlpatterns += router.urls

