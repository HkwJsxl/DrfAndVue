from django.urls import path
from sub_apps.serializer_related import views

urlpatterns = [
    # 数据校验
    path('index/', views.IndexView.as_view(), name='index_view'),
    path('index2/', views.Index2View.as_view(), name='index2_view'),
    # 序列化
    path('index3/', views.Index3View.as_view(), name='index3_view'),
    path('index4/', views.Index4View.as_view(), name='index4_view'),
    # 数据校验&序列化
    path('index5/', views.Index5View.as_view(), name='index5_view'),
]
