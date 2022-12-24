from django.shortcuts import render, HttpResponse, redirect

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning, AcceptHeaderVersioning, \
    HostNameVersioning, NamespaceVersioning


class ApiView(APIView):
    versioning_class = QueryParameterVersioning

    def get(self, request):
        current_version = request.version  # 查看请求的版本
        print(current_version)
        print(request.query_params)

        """反向生成url"""
        url = request.versioning_scheme.reverse('version_manage:api_view', request=request)
        print(url)
        url = request.versioning_scheme.reverse('version_manage:api_view2', args=('v10',), request=request)
        print(url)
        return Response({'status': 0, 'message': {'current_version': current_version}})

    def post(self, request):
        current_version = request.version
        accept_data = request.data
        print(accept_data)
        return Response({'status': 0, 'message': {'current_version': current_version, 'data': accept_data}})


class Api2View(APIView):
    versioning_class = URLPathVersioning

    def get(self, request, version):
        print(version)
        return Response({'status': 0, 'message': {'current_version': version}})


class Api3View(APIView):
    versioning_class = AcceptHeaderVersioning

    def get(self, request):
        current_version = request.version
        print(current_version)
        return Response({'status': 0, 'message': {'current_version': current_version}})
