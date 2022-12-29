from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from utils.exception_response import APIResponse


class TestView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return APIResponse(0, message={'get'})

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.serializer_class
