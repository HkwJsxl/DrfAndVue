from django.urls import path
from sub_apps.auth_permission import views

urlpatterns = [
    # 认证
    path('reg/', views.RegView.as_view(), name='reg_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('order/', views.OrderView.as_view(), name='order_view'),
    # 权限
    path('admin/', views.AdminView.as_view(), name='admin_view'),

    # 认证-token带在请求头里面
    path('token_login/', views.TokenHeaderLoginView.as_view({'post': 'post'}), name='token_login_view'),
]
