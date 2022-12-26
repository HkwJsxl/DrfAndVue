from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 2:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IDPermission(BasePermission):
    # 在请求进入视图之前就会执行。
    def has_permission(self, request, view):
        return True

    # 当视图中调用 `self.get_object`时就会被调用（删除、更新、查看某个对象时都会调用），
    # 一般用于检查对某个对象是否具有权限进行操作。
    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(view)  # 返回要进入的视图类
        print(obj)  # 数据库类对象
        return True

    """
    所以，让我们在编写视图类时，
    如果是直接获取间接继承了 GenericAPIView，同时内部调用 `get_object`方法，
    这样在权限中通过 `has_object_permission` 就可以进行权限的处理。
    """
