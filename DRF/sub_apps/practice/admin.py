from django.contrib import admin
from sub_apps.practice import models


admin.site.register(models.Book)
admin.site.register(models.Publish)
admin.site.register(models.Author)
admin.site.register(models.AuthorDetail)



