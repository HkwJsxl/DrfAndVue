from django.urls import path
from auth_permission import views

urlpatterns = [
    path('', views.ApiView.as_view(), name='api_view'),

]
