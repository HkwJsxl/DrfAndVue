import datetime

from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import filters, FilterSet, DjangoFilterBackend

from api import models
from api.extension import mixins
from api.seriazliers.comment import CommentModelSerializer, ListCommentModelSerializer
from api.extension.exception_response import APIResponse
from api.extension.auth import TokenHeaderAuthentication
from api.extension import return_code


class CommentFilterSet(FilterSet):
    latest_id = filters.NumberFilter(field_name='id', lookup_expr='lte')
    # news字段必传，不能数据库所有的评论
    news = filters.NumberFilter(field_name='news_id', required=True)

    class Meta:
        model = models.Comment
        fields = ('latest_id', 'news')


class CommentView(
    mixins.ReListModelMixin,
    mixins.ReCreateModelMixin,
    mixins.ReDestroyModelMixin,
    GenericViewSet
):
    # 查询评论时不需要登录，创建评论时需要登录
    authentication_classes = [TokenHeaderAuthentication, ]

    filter_backends = [DjangoFilterBackend, ]
    filterset_class = CommentFilterSet

    queryset = models.Comment.objects.all().order_by('-descendant_update_datetime')
    serializer_class = CommentModelSerializer

    def perform_create(self, serializer):
        user = self.request.user
        reply = serializer.validated_data.get('reply')
        root = serializer.validated_data.get('root')
        news = serializer.validated_data.get('news')
        if not reply:
            instance = models.Comment.objects.create(user=user, **serializer.validated_data)
        else:
            if news != reply.news:
                return APIResponse(return_code.AUTH_FAILED, {'errors': 'news或reply错误!'})
            # 更新根评论的最新后代更新时间
            if reply.root:
                # 传入的根评论要与数据库实际的根评论相吻合
                if reply.root != root:
                    return APIResponse(return_code.AUTH_FAILED, {'errors': '根评论错误!'})
                # 要回复的不是根评论
                reply.root.descendant_update_datetime = datetime.datetime.now()
                reply.root.save()
            else:
                # 要回复的是根评论
                # 是根评论时，要回复的评论必须是根评论的后代
                if reply != root:
                    return APIResponse(return_code.AUTH_FAILED, {'errors': '根评论错误!'})
                reply.descendant_update_datetime = datetime.datetime.now()
                reply.save()
            # 回复评论时要将当前评论深度在原评论深度基础上加1
            parent_depth = reply.depth
            instance = models.Comment.objects.create(user=user, **serializer.validated_data)
            instance.depth = parent_depth + 1
            instance.save()
        instance.news.comment_count += 1
        instance.news.save()
        return APIResponse()

    def perform_destroy(self, instance):
        instance.delete()
        instance.news.comment_count -= 1
        instance.news.save()

    def get_authenticators(self):
        if self.request.method == 'GET':
            return []
        return super(CommentView, self).get_authenticators()

    # 第二种数据的展示方式
    def get_serializer_class(self):
        """根据请求方式的不同应用不同的类"""
        if self.request.method == 'GET':
            return ListCommentModelSerializer
        return self.serializer_class
