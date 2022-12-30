from rest_framework import serializers
from sub_apps.practice import models


class TestGetSerializer(serializers.Serializer):
    ...


class TestPostSerializer(serializers.Serializer):
    ...


class BookListSerializer(serializers.ListSerializer):
    # many=True
    def update(self, instance, validated_data):
        return [
            self.child.update(instance[i], attrs) for i, attrs in enumerate(validated_data)
        ]


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = BookListSerializer

        model = models.Book
        fields = (
            # 'pk',
            'name',
            'price',
            'publish',
            'authors',
            'publish_name',
            'author_list',
        )
        extra_kwargs = {
            'pk': {'write_only': True},
            'publish': {'write_only': True},
            'authors': {'write_only': True}
        }
