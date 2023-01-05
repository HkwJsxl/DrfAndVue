import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from django.contrib.auth.models import User


class UserRegModelSerializer(serializers.ModelSerializer):
    """用户注册"""

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if re.match(r'^[a-zA-Zd_.-]+@[a-zA-Zd-]+(\.[a-zA-Zd-]+)*\.[a-zA-Zd]{2,6}$', username):
            name = username.split('@')[0]
            obj = User.objects.create_user(username=name, email=username, password=password)
            return obj
        obj = User.objects.create_user(username=username, password=password)
        return obj


class UserLoginModelSerializer(serializers.ModelSerializer):
    """用户多方式登录"""

    # 必须重写username字段
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if re.match(r'^[a-zA-Zd_.-]+@[a-zA-Zd-]+(\.[a-zA-Zd-]+)*\.[a-zA-Zd]{2,6}$', username):
            obj = User.objects.filter(email=username).first()
        else:
            obj = User.objects.filter(username=username).first()
        if not obj:
            raise ValidationError('用户不存在.')
        else:
            if not obj.check_password(password):
                raise ValidationError('密码错误.')
            else:
                # 密码正确，签发token
                payload = jwt_payload_handler(obj)
                token = jwt_encode_handler(payload)
                # views中可以取出来
                self.context['token'] = token
                self.context['username'] = obj.username
        return attrs
