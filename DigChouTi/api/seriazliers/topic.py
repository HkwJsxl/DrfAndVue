from rest_framework import serializers
from api import models


class TopicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ('pk', 'title', 'is_hot', 'create_datetime')

        extra_kwargs = {
            'pk': {'read_only': True},
            'is_hot': {'read_only': True},
            'create_datetime': {'read_only': True}
        }
