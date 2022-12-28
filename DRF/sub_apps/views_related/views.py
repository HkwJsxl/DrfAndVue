from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.viewsets import ViewSet, ViewSetMixin
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser

from sub_apps.views_related import models
from sub_apps.views_related import ser_view
from utils.permission_related import IDPermission
from utils.filter_related import CustomFilter, UserFilterSet, UserFilterSet2
from sub_apps.views_related.ser_view import UserModelSerializer
from utils.page_related import (
    UserPageNumberPagination,
    UserCursorPagination,
    UserModelPageNumberPagination,
    UserModelLimitOffsetPagination,
    UserModelCursorPagination
)


class UserModelView(ModelViewSet):
    permission_classes = [IDPermission, ]

    # ModelViewSet包括所有的增删改查ModelMixin
    queryset = models.UserInfo.objects.all()
    serializer_class = ser_view.UserModelSerializer

    # 重写功能方法
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 0, 'message': {'data': serializer.data}})

    def perform_create(self, serializer):
        serializer.save(password='123456', email="create@create.com")  # 不校验的字段要自己传值

    def perform_update(self, serializer):
        serializer.save(password='666', email='new@new.com')  # 不校验的字段要自己传值


class UserFilterModelView(ModelViewSet):
    # 筛选类
    filter_backends = [CustomFilter, ]
    queryset = models.UserInfo.objects.all()
    serializer_class = ser_view.UserModelSerializer


class UserFilter2ModelView(ModelViewSet):
    filter_backends = [DjangoFilterBackend, ]
    # filterset_fields = ['id', 'age']
    # filterset_class = UserFilterSet
    filterset_class = UserFilterSet2

    queryset = models.UserInfo.objects.all()
    serializer_class = ser_view.UserModelSerializer


# 内置筛选
class UserFilter3ModelView(ModelViewSet):
    filter_backends = [OrderingFilter, ]
    ordering_param = 'order'  # ?order=xxx
    ordering_fields = ["id", "age"]

    # filter_backends = [SearchFilter, ]
    # search_fields = ["id", "username"]

    queryset = models.UserInfo.objects.all()
    serializer_class = ser_view.UserModelSerializer


class UserPageModelView(APIView):
    def get(self, request):
        queryset = models.UserInfo.objects.all().order_by('pk')
        # setting.py---PAGE_SIZE
        # pager = PageNumberPagination()  # http://127.0.0.1:8000/views_related/users/page/?page=2

        # pager = UserPageNumberPagination()  # http://127.0.0.1:8000/views_related/users/page/?size=3
        # pager = LimitOffsetPagination()  # http://127.0.0.1:8000/views_related/users/page/?limit=3&offset=1
        pager = UserCursorPagination()  # http://127.0.0.1:8000/views_related/users/page/?limit=3&offset=1
        paginate_queryset = pager.paginate_queryset(queryset, request, self)
        ser = UserModelSerializer(instance=paginate_queryset, many=True)
        return Response(ser.data)


class UserPage2ModelView(ModelViewSet):
    # http://127.0.0.1:8000/views_related/users/page2/?size=3
    # pagination_class = UserModelPageNumberPagination
    # http://127.0.0.1:8000/views_related/users/page2/?offset=2&limit=3
    # pagination_class = UserModelLimitOffsetPagination
    #
    pagination_class = UserModelCursorPagination

    queryset = models.UserInfo.objects.all().order_by('pk')
    serializer_class = ser_view.UserModelSerializer


class UserRouterModelView(ModelViewSet):
    # 默认前三个解析器
    parser_classes = [JSONParser, FormParser, MultiPartParser, FileUploadParser]
    queryset = models.UserInfo.objects.all().order_by('pk')
    serializer_class = ser_view.UserModelSerializer


class UserParserView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser, FileUploadParser]

    def post(self, request, *args, **kwargs):
        print(request.content_type)
        print(request.data)
        print(request.data.get('file'))
        return Response({'status': 0})


class Top5ModelView(ModelViewSet):
    queryset = models.UserInfo.objects.all().order_by('pk')[:5]
    serializer_class = ser_view.UserModelSerializer

    def list(self, request, *args, **kwargs):
        return super(Top5ModelView, self).list(request, *args, **kwargs)
