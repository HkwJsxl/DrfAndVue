from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api import models


class NewsModelSerializer(serializers.ModelSerializer):
    """新闻资讯"""

    topic_title = serializers.CharField(source='topic.title', read_only=True)
    zone_title = serializers.CharField(source='get_zone_display', read_only=True)
    status_info = serializers.CharField(source='get_status_display', read_only=True)
    image_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.News
        fields = (
            'title',
            'url',
            'image',
            'zone',
            'topic',
            'create_datetime',
            'collect_count',
            'recommend_count',
            'comment_count',

            'topic_title',
            'zone_title',
            'status_info',
            'image_list',
        )

        read_only_fields = ('create_datetime', 'collect_count', 'recommend_count', 'comment_count')
        extra_kwargs = {
            'status': {'write_only': True},
            'zone': {'write_only': True},
            'topic': {'write_only': True},
            'image': {'write_only': True}
        }

    def get_image_list(self, obj):
        if not obj.image:
            return None
        return obj.image.split(',')

    def validate_topic(self, obj):
        # 专区可以为空
        if not obj:
            raise ValidationError('必须选择一个专区!')
        request = self.context['request']
        # 专区不能是别人的，并且必须存在
        is_exists = models.Topic.objects.filter(pk=obj.pk, user=request.user, deleted=False).exists()
        if not is_exists:
            raise ValidationError('topic does not exist!')
        return obj

    def validate(self, attrs):
        url = self.initial_data.get('url')
        image = self.initial_data.get('image')
        zone = self.initial_data.get('zone')
        # 不能既有图片又有链接
        if url and image:
            raise ValidationError('数据错误!')
        # 仅有文本不能选择 图片专区
        if not url and not image:
            # 专区3：图片
            if zone == 3:
                raise ValidationError('专区选择错误!')
        return attrs

    def create(self, validated_data):
        # print(self.context)
        # self.context中有三个值
        # {
        # 'request': <rest_framework.request.Request: POST '/api/news/'>,
        # 'format': None,
        # 'view': <api.views.news.NewsView object at 0x0000024E686CE400>
        # }
        request = self.context['request']
        # 创建咨询，并自己做一个推荐
        news_obj = models.News.objects.create(recommend_count=1, **validated_data)
        # 推荐记录
        models.Recommend.objects.create(news=news_obj, user=request.user)
        return news_obj  # 后续可以直接点点点，不用obj.get()取值
