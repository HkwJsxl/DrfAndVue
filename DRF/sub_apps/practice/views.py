from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from utils.exception_response import APIResponse
from sub_apps.practice.ser import TestGetSerializer, TestPostSerializer


class TestView(GenericAPIView):
    queryset = None
    serializer_class = TestGetSerializer
    post_serializer_class = TestPostSerializer

    def get(self, request, *args, **kwargs):
        tp = type(self.get_serializer())
        return APIResponse(0, message=str(tp))

    def post(self, request, *args, **kwargs):
        tp = type(self.get_serializer())
        return APIResponse(0, message=str(tp))

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return self.serializer_class
        elif method == 'POST':
            return self.post_serializer_class
        else:
            return APIResponse(1, '请求不允许!')
