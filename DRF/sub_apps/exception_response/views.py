from rest_framework.views import APIView
from utils.exception_response import APIResponse


class ApiView(APIView):
    def get(self, request, *args, **kwargs):
        return APIResponse(0, {'get': 'api_view'})
