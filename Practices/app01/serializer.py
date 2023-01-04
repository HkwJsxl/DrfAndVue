import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app01 import models


class UserCreateModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=8, max_length=18, required=True, write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ('id', 'username', 'mobile', 'icon', 'password', 'confirm_password')
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def validate_mobile(self, value):
        if not re.search('^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$', value):
            raise ValidationError('手机号格式错误.')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')
        if password != confirm_password:
            raise ValidationError('两次密码输入不一致.')
        return attrs

    def create(self, validated_data):
        return models.UserInfo.objects.create_user(**validated_data)


class UserRetrieveModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ('id', 'username', 'mobile', 'icon')


class UserUpdateModelSerializer(serializers.ModelSerializer):
    """只更新头像"""

    class Meta:
        model = models.UserInfo
        fields = ('id', 'username', 'mobile', 'icon')
        read_only_fields = ('id', 'username', 'mobile')
        extra_kwargs = {
            'icon': {
                'write_only': True,
                'required': True,
            },
        }
