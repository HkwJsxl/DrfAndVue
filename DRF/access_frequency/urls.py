from django.urls import path
from access_frequency import views

urlpatterns = [
    path('throttle/', views.ThrottleView.as_view(), name='throttle_view'),


]
