from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('app01/', include(('app01.urls', 'app01'), namespace='app01'))


]
