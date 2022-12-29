from django.urls import path, include
from sub_apps.practice import views

from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'router', views.UserRouterModelView)

urlpatterns = [
    # 视图类继承GenericAPIView，get方法，post方法，用的序列化类不一样（重写get_serializer_class）
    path('test1/', views.TestView.as_view()),
    # 图书一堆关联表的增删查改
]

# urlpatterns += router.urls
