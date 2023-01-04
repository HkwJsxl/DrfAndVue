from django.urls import path
from app01 import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('user', views.UserCreateGenericViewSet)


urlpatterns = [

]

urlpatterns += router.urls
