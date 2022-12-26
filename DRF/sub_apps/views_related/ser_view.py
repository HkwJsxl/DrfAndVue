from rest_framework import serializers
from sub_apps.serializer_related import models


class UserModelSerializer(serializers.ModelSerializer):
    model = models.UserInfo
    fields = [
        'pk',
        'username',
        'password',
        'age',
        'email',
    ]
