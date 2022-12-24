from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import QueryParameterVersioning


class ApiView(APIView):
    versioning_class = QueryParameterVersioning

    def get(self, request):
        current_version = request.version  # 查看请求的版本
        print(current_version)
        print(request.query_params)

        return Response({'status': 0, 'message': {'current_version': current_version}})

    def post(self, request):
        current_version = request.version
        accept_data = request.data
        print(accept_data)
        return Response({'status': 0, 'message': {'current_version': current_version, 'data': accept_data}})
