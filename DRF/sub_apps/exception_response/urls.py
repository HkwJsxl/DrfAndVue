from django.urls import path, include
from sub_apps.exception_response import views

from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'router', views.UserRouterModelView)

urlpatterns = [
    path('', views.ApiView.as_view()),
]

# urlpatterns += router.urls
