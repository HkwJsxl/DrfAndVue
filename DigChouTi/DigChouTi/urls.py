from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls

# 添加 get_schema_view 辅助函数
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

# 参数 title 为接口网站标题
schema_view = get_schema_view(title='代码改变生活', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', 'api'), namespace='api')),

    # 自动生成接口文档
    # coreapi
    path('docs/', include_docs_urls(title='代码改变生活', description='自动生成接口文档')),

    # swagger
    # path('docs/', schema_view, name='docs'),
]
