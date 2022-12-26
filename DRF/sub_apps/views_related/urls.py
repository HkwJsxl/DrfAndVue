from django.urls import path
from sub_apps.views_related import views

urlpatterns = [
    path('users/', views.UserModelView.as_view(actions={
        'get': 'list',
        'post': 'create',
    }), name='user_view'),
    path('users/<int:pk>/', views.UserModelView.as_view(actions={
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='user_view'),

]
