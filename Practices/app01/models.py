import os

from django.db import models
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    return os.path.join('user_dir_path', instance.username, "icon", filename)


class UserInfo(AbstractUser):
    # 手机号，创建唯一约束
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True, blank=True, unique=True)
    # 头像
    icon = models.ImageField(verbose_name='头像', default='/static/images/default.png', upload_to=user_directory_path)
