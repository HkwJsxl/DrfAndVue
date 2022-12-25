from rest_framework import serializers

from serializer_related import models


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=18, label='用户名')
    password = serializers.CharField(min_length=3, max_length=18, label='密码')
    age = serializers.IntegerField(label='年龄')
    email = serializers.EmailField(label='邮箱')
    level = serializers.ChoiceField(choices=models.UserInfo.level_choices, default=1, label='级别')
    roles = serializers.IntegerField(default=1)
    depart = serializers.IntegerField(default=1)


class User2Serializer(serializers.Serializer):
    class Meta:
        models = models.UserInfo
        fields = [
            'username',
            'password',
            'age',
            'email',
        ]
        extra_kwargs = {
            'username': {'min_length': 3, 'max_length': 18},
        }
