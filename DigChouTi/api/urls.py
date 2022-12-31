from django.urls import path
from api.views import account

from rest_framework import routers

router = routers.SimpleRouter()
# 注册
router.register(r'register', account.RegView, 'register')
# 登录
# router.register(r'login', account.LoginView, 'login')

urlpatterns = [
    # 登录
    path('login/', account.LoginView.as_view(), name='login')
]

urlpatterns += router.urls
