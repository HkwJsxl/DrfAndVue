from django.urls import path
from sub_apps.access_frequency import views

urlpatterns = [
    path('throttle/', views.IndexView.as_view(), name='throttle_view'),


]
