from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from utils.exception_response import APIResponse
from sub_apps.practice.ser import TestGetSerializer, TestPostSerializer, BookModelSerializer
from sub_apps.practice import models


class TestView(GenericAPIView):
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


class BookAPIView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            # 查看一条
            obj = models.Book.objects.filter(pk=pk, is_delete=False).first()
            ser = BookModelSerializer(instance=obj)
        else:
            # 查看多条
            obj = models.Book.objects.all().filter(is_delete=False)
            ser = BookModelSerializer(instance=obj, many=True)
        return APIResponse(0, data=ser.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, dict):
            # 创建一条
            ser = BookModelSerializer(data=data)
        elif isinstance(data, list):
            # 创建多条
            ser = BookModelSerializer(data=data, many=True)
        else:
            return APIResponse(0, '传入数据不符合规范!')
        if not ser.is_valid():
            return APIResponse(1005, '数据校验失败!')
        ser.save()
        return APIResponse(data=ser.data)

    # def put(self, request, pk=None, *args, **kwargs):
    #     """
    #     格式
    #     {
    #         "name": "Python全栈1",
    #         "price": "33.66",
    #         "publish": 2,
    #         "authors": [
    #             2
    #         ]
    #     }
    #     """
    #     data = request.data
    #     if isinstance(data, dict):
    #         # 修改一条
    #         obj = models.Book.objects.filter(pk=pk, is_delete=False).first()
    #         ser = BookModelSerializer(instance=obj, data=request.data)
    #         if not ser.is_valid():
    #             return APIResponse(1005, '数据校验失败!')
    #         ser.save()
    #         return APIResponse(data=ser.data)
    #     elif isinstance(data, list):
    #         # 修改多条
    #         ser_data_list = []
    #         for item in data:
    #             pk = item.get('pk')
    #             obj = models.Book.objects.filter(pk=pk, is_delete=False).first()
    #             ser = BookModelSerializer(instance=obj, data=item)
    #             if not ser.is_valid():
    #                 return APIResponse(1005, '数据校验失败!')
    #             ser.save()
    #             ser_data_list.append(ser.data)
    #         return APIResponse(data=ser_data_list)
    #     else:
    #         return APIResponse(0, '传入数据不符合规范!')

    # 修改多条方法2,ser写list_serializer_class，重写update，继承serializers.ListSerializer
    def put(self, request, pk=None, *args, **kwargs):
        data = request.data
        if isinstance(data, dict):
            # 修改一条
            obj = models.Book.objects.filter(pk=pk, is_delete=False).first()
            ser = BookModelSerializer(instance=obj, data=request.data)
            if not ser.is_valid():
                return APIResponse(1005, '数据校验失败!')
            ser.save()
            return APIResponse(data=ser.data)
        elif isinstance(data, list):
            # 修改多条
            obj_list = []
            modify_data_list = []
            for item in data:
                pk = item.get('pk')
                obj = models.Book.objects.filter(pk=pk, is_delete=False).first()
                obj_list.append(obj)
                modify_data_list.append(item)
            ser = BookModelSerializer(instance=obj_list, data=modify_data_list, many=True)
            if not ser.is_valid():
                return APIResponse(1005, '数据校验失败!')
            ser.save()
            return APIResponse(data=ser.data)
        else:
            return APIResponse(0, '传入数据不符合规范!')

    def delete(self, request, pk=None, *args, **kwargs):
        """格式：{"pk": 1}或{"pk": [3,4]}或http://127.0.0.1:8000/practice/books/1/"""
        if pk:
            ret_num = models.Book.objects.filter(pk=pk, is_delete=False).update(is_delete=True)
        else:
            try:
                pk = request.data.get('pk')
                if isinstance(pk, int):
                    ret_num = models.Book.objects.filter(pk=pk, is_delete=False).update(is_delete=True)
                elif isinstance(pk, list):
                    ret_num = models.Book.objects.filter(pk__in=pk, is_delete=False).update(is_delete=True)
                else:
                    return APIResponse(1, 'pk值传入不正确!---%s')
            except Exception as e:
                return APIResponse(1, '删除失败!---%s' % e)
        return APIResponse(0, {'del_num': ret_num})
