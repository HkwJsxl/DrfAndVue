from django.db import models


class UserInfo(models.Model):
    role_choices = ((1, "普通用户"), (2, "管理员"), (3, "超级管理员"),)
    role = models.IntegerField(verbose_name="角色", choices=role_choices, default=1)

    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)

    def __str__(self):
        return self.username
