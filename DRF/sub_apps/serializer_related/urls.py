from django.urls import path
from sub_apps.serializer_related import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index_view'),
    path('index2/', views.Index2View.as_view(), name='index2_view'),


]
