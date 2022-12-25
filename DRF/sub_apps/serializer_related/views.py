from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from sub_apps.serializer_related.ser import UserSerializer, User2Serializer


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
        ser_obj = User2Serializer(data=request.data)
        if not ser_obj.is_valid():
            return Response({'status': 0, 'message': {'data': ser_obj.errors}})

        print(ser_obj.validated_data)
        return Response({'status': 0, 'message': '校验成功'})
