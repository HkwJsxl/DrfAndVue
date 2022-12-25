from django.urls import path
from version_manage import views

urlpatterns = [
    path('', views.ApiView.as_view(), name='api_view'),
    path('header/', views.Api3View.as_view(), name='api_view3'),

    path('<str:version>/', views.Api2View.as_view(), name='api_view2'),

]
