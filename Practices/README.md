# 练习项目

## 介绍

- app01
    ~~~
  自定义User表，新增mobile唯一约束字段；新增icon图片字段
	在自定义User表基础上，用 GenericViewSet + CreateModelMixin + serializer 完成User表新增接口（就是注册接口）
  （重要提示：序列化类要重写create方法，不然密码就是明文了）
	在自定义User表基础上，用 GenericViewSet + RetrieveModelMixin + serializer 完成User表单查（就是用户中心）
	在自定义User表基础上，用 GenericViewSet + UpdateModelMixin + serializer 完成用户头像的修改
	~~~

