from django.urls import path
from sub_apps.views_related import views

urlpatterns = [
    path('users/', views.UserModelView.as_view(), name='user_view'),
    path('users/<int:pk>', views.UserModelView.as_view(), name='user_view'),

]
