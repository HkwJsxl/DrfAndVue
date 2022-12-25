from django.forms.models import model_to_dict

from rest_framework import serializers

from sub_apps.serializer_related import models


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=18, label='用户名')
    password = serializers.CharField(min_length=3, max_length=18, label='密码')
    age = serializers.IntegerField(label='年龄')
    email = serializers.EmailField(label='邮箱')
    level = serializers.ChoiceField(choices=models.UserInfo.level_choices, default=1, label='级别')
    roles = serializers.IntegerField(default=1)
    depart = serializers.IntegerField(default=1)


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = [
            'username',
            'password',
            'age',
            'email',
            'depart'
        ]
        extra_kwargs = {
            'username': {'min_length': 3, 'max_length': 18},
        }

    def create(self, validated_data):
        # print('validated_data: ', validated_data)
        return models.UserInfo.objects.create(**validated_data)


class Index3ModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(source='get_level_display')
    depart = serializers.CharField(source='depart.title')
    roles = serializers.SerializerMethodField()
    extra = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo
        fields = [
            'pk',
            'username',
            'password',
            'age',
            'level_text',
            'depart',
            'roles',
            'extra',
        ]

    def get_roles(self, obj):
        role_queryset = obj.roles.all()
        return [model_to_dict(item, ['id', 'title']) for item in role_queryset]

    def get_extra(self, obj):
        return 'extra'
