from django.urls import path, include
from sub_apps.views_related import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'router', views.UserRouterModelView, basename='router')

urlpatterns = [
    # 视图
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
    # 筛选
    # 1.自定义筛选
    path('users/filter/', views.UserFilterModelView.as_view(actions={
        'get': 'list',
    }), name='user_filter_view'),
    # 2.第三方筛选
    path('users/filter2/', views.UserFilter2ModelView.as_view(actions={
        'get': 'list',
    }), name='user_filter2_view'),
    # 3.内置筛选
    path('users/filter3/', views.UserFilter3ModelView.as_view(actions={
        'get': 'list',
    }), name='user_filter3_view'),

    # 分页
    path('users/page/', views.UserPageModelView.as_view(), name='user_page_view'),
    path('users/page2/', views.UserPage2ModelView.as_view(actions={
        'get': 'list',
    }), name='user_page2_view'),

    # router
    path('api/', include(router.urls)),

    # parser
    path('users/parser/', views.UserParserView.as_view(), name='user_parser_view'),

    # 获取前五条数据
    path('top5/', views.Top5ModelView.as_view(actions={
        'get': 'list',
    }), name='top5_view'),
]

# urlpatterns += router.urls
