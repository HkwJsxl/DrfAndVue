from django.forms.models import model_to_dict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class DepartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class RoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class Index4ModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(source='get_level_display')
    depart = DepartModelSerializer()  # 一对多
    roles = RoleModelSerializer(many=True)  # 多对多：many=True

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
        ]


class Depart2ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': False},
            'title': {'read_only': True},
        }


class Role2ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': False},
            'title': {'read_only': True},
        }


class Index5ModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(source='get_level_display', read_only=True)  # 用户等级，用户自己不能修改
    depart = Depart2ModelSerializer()
    roles = Role2ModelSerializer(many=True)

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
        ]
        extra_kwargs = {
            'age': {'read_only': True},  # 用户不能更改
            # 'age': {'read_only': False},  # 用户可以更改
        }

    def validate_username(self, value):
        if value in ['666', '777']:
            raise ValidationError({'status': 1005, 'message': '用户名检验失败!'})
        return value

    def create(self, validated_data):
        depart_id = validated_data.pop('depart').get('id')
        validated_data['depart_id'] = depart_id
        role_id_list = [ele.get('id') for ele in validated_data.pop('roles')]
        user_obj = models.UserInfo.objects.create(**validated_data)
        for role_id in role_id_list:
            models.Userinfo2Roles.objects.create(user=user_obj, role_id=role_id)
        return user_obj
