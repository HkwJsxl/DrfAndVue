from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api import models


class CollectTopicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ('id', 'title', 'is_hot')


class CollectNewsModelSerializer(serializers.ModelSerializer):
    """收藏"""

    zone = serializers.CharField(source='get_zone_display')
    topic = CollectTopicModelSerializer()
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


class CollectModelSerializer(serializers.ModelSerializer):
    news_info = CollectNewsModelSerializer(read_only=True, source='news')

    class Meta:
        model = models.Collect
        fields = ('id', 'create_datetime', 'news', 'news_info')
        extra_kwargs = {
            'id': {'read_only': True},
            'news': {'write_only': True},
        }

    def validate_news(self, obj):
        if obj.deleted:
            raise ValidationError('news not exist!')
        return obj
