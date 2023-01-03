from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api import models


class CommentTopicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ('id', 'title', 'is_hot')


class CommentNewsModelSerializer(serializers.ModelSerializer):
    zone = serializers.CharField(source='get_zone_display')
    topic = CommentTopicModelSerializer()
    image_list = serializers.SerializerMethodField()

    class Meta:
        model = models.News
        fields = (
            'title',
            'url',
            'image',
            'zone',
            'create_datetime',
            'topic',
            'collect_count',
            'recommend_count',
            'comment_count',

            'image_list',
        )
        read_only_fields = ('create_datetime', 'collect_count', 'recommend_count', 'comment_count')

    def get_image_list(self, obj):
        if not obj.image:
            return obj.image
        return obj.image.split(',')


class CommentModelSerializer(serializers.ModelSerializer):
    """评论"""
    news_info = CommentNewsModelSerializer(source='news', read_only=True)
    root_content = serializers.SerializerMethodField(read_only=True)
    reply_content = serializers.SerializerMethodField(read_only=True)

    # 定义日期格式
    create_datetime = serializers.DateTimeField(format='%Y-%m-%d %X', read_only=True)
    descendant_update_datetime = serializers.DateTimeField(format='%Y-%m-%d %X', read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'content',
            'depth',
            'create_datetime',
            'descendant_update_datetime',
            'news',
            'root',
            'reply',

            'news_info',
            'root_content',
            'reply_content',
        )
        extra_kwargs = {
            'news': {'write_only': True},
            'root': {'write_only': True},
            'reply': {'write_only': True},
        }

    def get_root_content(self, obj):
        if not obj.root:
            return None
        return obj.root.content

    def get_reply_content(self, obj):
        if not obj.reply:
            return None
        return obj.reply.content

    def validate(self, attrs):
        root = self.initial_data.get('root')
        reply = self.initial_data.get('reply')
        if not root and not reply:
            return attrs
        if not root or not reply:
            raise ValidationError('要同时提交跟评论和子评论!')
        return attrs


class CreateCommentSerializer(serializers.ModelSerializer):
    create_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = models.Comment
        fields = ['news', 'reply', 'content', 'depth', 'create_datetime']
        read_only_fields = ['depth', ]
        extra_kwargs = {'news': {'write_only': True}}


class ListCommentModelSerializer(serializers.ModelSerializer):
    create_datetime = serializers.DateTimeField(format='%Y-%m-%d %X', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ['create_datetime', 'reply', 'content', 'children']

    def get_children(self, obj: object = '每一个评论对象'):
        # 获取当前根评论的所有的子孙评论
        descendant_queryset = models.Comment.objects.filter(root=obj).order_by('id')

        descendant_dict = {}
        for descendant in descendant_queryset:
            ser = CreateCommentSerializer(instance=descendant, many=False)
            row = {'children': []}
            row.update(ser.data)
            descendant_dict[descendant.id] = row

        # 根评论对象的1级评论
        children_list = []
        for cid, item in descendant_dict.items():
            depth = item['depth']
            if depth == 1:
                children_list.append(item)
                continue
            reply_id = item['reply']
            descendant_dict[reply_id]['children'].append(item)

        return children_list
