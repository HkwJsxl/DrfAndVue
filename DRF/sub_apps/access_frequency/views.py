from rest_framework.views import APIView
from rest_framework.response import Response

from utils.throttle_related import RateThrottle


class IndexView(APIView):
    throttle_classes = [RateThrottle, ]

    def get(self, request):
        return Response({'status': 0, 'message': '通过访问限制'})
