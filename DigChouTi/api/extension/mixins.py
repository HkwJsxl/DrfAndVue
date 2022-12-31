from rest_framework import mixins

from api.extension import return_code
from api.extension.exception_response import APIResponse


class ReCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(return_code.VALIDATE_ERROR, data=serializer.errors)
        res = self.perform_create(serializer)
        return res or APIResponse(data=serializer.data)


class ReListModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return APIResponse(data=serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(data=serializer.data)


class ReUpdateModelMixin(mixins.UpdateModelMixin):
    def list(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return APIResponse(return_code.VALIDATE_ERROR, data=serializer.errors)
        res = self.perform_update(serializer)
        return res or APIResponse(data=serializer.data)


class ReDestroyModelMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        res = self.perform_destroy(instance)
        return res or APIResponse()
