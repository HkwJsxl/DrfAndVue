from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ViewSetMixin, GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from sub_apps.serializer_related import models
from sub_apps.views_related import ser_view


class UserModelView(GenericAPIView):
    queryset = models.UserInfo
    serializer_class = ser_view.UserModelSerializer

