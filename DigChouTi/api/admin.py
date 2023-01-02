from django.contrib import admin

from api import models

admin.site.register(models.UserInfo)
admin.site.register(models.Topic)
admin.site.register(models.News)
admin.site.register(models.Collect)
admin.site.register(models.Recommend)
admin.site.register(models.Comment)
