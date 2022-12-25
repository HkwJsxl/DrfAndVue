from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response


class IndexView(APIView):
    def get(self, request):
        return Response({'status': 0, 'message': 'get'})

    def post(self, request):
        return Response({'status': 0, 'message': 'post'})
