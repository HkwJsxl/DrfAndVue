from rest_framework import mixins
from rest_framework.response import Response

from api.extension import return_code
from api.extension.exception_response import APIResponse


class ReCreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(return_code.VALIDATE_ERROR, serializer.errors)
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
