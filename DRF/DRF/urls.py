from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('version_manage/', include(('version_manage.urls', 'version_manage'), namespace='version_manage')),
    path('auth_permission/', include(('auth_permission.urls', 'auth_permission'), namespace='auth_permission')),
    path('access_frequency/', include(('access_frequency.urls', 'access_frequency'), namespace='access_frequency')),

]
