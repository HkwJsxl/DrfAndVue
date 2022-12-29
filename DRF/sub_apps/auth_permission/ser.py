from rest_framework import serializers

from sub_apps.auth_permission import models


class UserSerializers(serializers.ModelSerializer):
    model = models.UserInfo
    fields = '__all__'
