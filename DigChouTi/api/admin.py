from django.contrib import admin

from api import models

admin.site.register(models.UserInfo)
admin.site.register(models.Topic)
