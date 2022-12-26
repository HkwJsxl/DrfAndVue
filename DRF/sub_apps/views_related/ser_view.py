from rest_framework import serializers
from sub_apps.views_related import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )

    class Meta:
        model = models.UserInfo
        fields = [
            'pk',
            'username',
            'age',
            'level_text',
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # 密码不能返回
        }
