from django.urls import path
from auth_permission import views

urlpatterns = [
    path('reg/', views.RegView.as_view(), name='reg_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('order/', views.OrderView.as_view(), name='order_view'),

]
