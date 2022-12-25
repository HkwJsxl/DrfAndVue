from django.urls import path
from auth_permission import views

urlpatterns = [
    # 认证
    path('reg/', views.RegView.as_view(), name='reg_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('order/', views.OrderView.as_view(), name='order_view'),
    # 权限
    path('admin/', views.AdminView.as_view(), name='admin_view'),

]
