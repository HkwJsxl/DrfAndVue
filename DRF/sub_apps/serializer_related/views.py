from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from sub_apps.serializer_related.ser import UserSerializer, UserModelSerializer, Index3ModelSerializer, \
    Index4ModelSerializer, Index5ModelSerializer
from sub_apps.serializer_related import models


class IndexView(APIView):
    def post(self, request):
        # 多传的直接忽略
        # postman：{"username": "hkw", "password": "123", "age": 18, "email": "hkwJsxl@gmail.com", "other": "666"}
        ser_obj = UserSerializer(data=request.data)
        if not ser_obj.is_valid():
            return Response({'status': 0, 'message': {'data': ser_obj.errors}})
        print(ser_obj.validated_data)
        # OrderedDict([('username', 'hkw'), ('password', '123'), ('age', 18), ('email', 'hkwJsxl@gmail.com'), ('level', 1)])
        return Response({'status': 0, 'message': '校验成功'})


class Index2View(APIView):
    def post(self, request):
        print(request.data)
        ser_obj = UserModelSerializer(data=request.data)
        if not ser_obj.is_valid():
            return Response({'status': 1005, 'message': {'data': ser_obj.errors}})
        ser_obj.save()
        print(ser_obj.validated_data)
        return Response({'status': 0, 'message': '校验成功'})


class Index3View(APIView):
    def get(self, request):
        user_queryset = models.UserInfo.objects.all()
        ser_obj = Index3ModelSerializer(instance=user_queryset, many=True)
        return Response({'status': 0, 'message': {'data': ser_obj.data}})


class Index4View(APIView):
    def get(self, request):
        user_queryset = models.UserInfo.objects.all()
        ser_obj = Index4ModelSerializer(instance=user_queryset, many=True)
        return Response({'status': 0, 'message': {'data': ser_obj.data}})


class Index5View(APIView):
    def get(self, request):
        user_queryset = models.UserInfo.objects.all()
        ser_obj = Index5ModelSerializer(instance=user_queryset, many=True)
        return Response({'status': 0, 'message': {'data': ser_obj.data}})

    def post(self, request):
        ser_obj = Index5ModelSerializer(data=request.data)
        if not ser_obj.is_valid():
            return Response({'status': 1005, 'message': {'data': ser_obj.errors}})
        ser_obj.save()
        print(ser_obj.data)
        return Response({'status': 0, 'message': {'data': ser_obj.data}})
