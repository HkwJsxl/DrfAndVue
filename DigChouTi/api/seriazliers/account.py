import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api import models


class RegModelSerializer(serializers.ModelSerializer):
    """注册"""
    password = serializers.CharField(label='密码', min_length=8, max_length=18, write_only=True)
    confirm_password = serializers.CharField(label='确认密码', min_length=8, max_length=18, write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ('username', 'phone', 'password', 'confirm_password')

    def validate_username(self, value):
        exists = models.UserInfo.objects.filter(username=value, deleted=False).exists()
        if exists:
            raise ValidationError("用户名已存在!")
        return value

    def validate_phone(self, value):
        ret = re.search(r'^1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}$', value)
        if not ret:
            raise ValidationError('手机号格式错误!')
        exists = models.UserInfo.objects.filter(phone=value, deleted=False).exists()
        if exists:
            raise ValidationError("手机号已存在!")
        return value

    def validate(self, attrs):
        # 有ValidationError不通过的信息
        # print(attrs)
        # 最初的信息，没有校验
        # print(self.initial_data)
        password = self.initial_data.get('password')
        confirm_password = self.initial_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('两次密码输入不同!')
        return attrs


class LoginModelSerializer(serializers.Serializer):
    """登录"""
    username = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True, min_length=8, max_length=18)

    def validate(self, attrs):
        username = self.initial_data.get('username')
        phone = self.initial_data.get('phone')
        if not username and not phone:
            raise ValidationError('请提交用户名或手机号!')
        if username and phone:
            raise ValidationError('用户名或手机号不能同时提交!')
        return attrs
