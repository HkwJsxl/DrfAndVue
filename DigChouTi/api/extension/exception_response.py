from rest_framework.views import exception_handler
from rest_framework.response import Response

from api.extension import return_code


def re_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if not response:
        return APIResponse(1, 'errors: %s' % str(exc))
    return APIResponse(1, response.data.get('detail'))


class APIResponse(Response):
    def __init__(self, code=return_code.SUCCESS, message='OK', data=None, *args, **kwargs):
        """
        统一格式
        {
            "code": 0,
            "message": "OK",
            "data": []
        }
        """
        res_dict = {'code': code, 'message': message, 'data': data}

        """data为空时不返回data属性"""
        # res_dict = {'code': code, 'message': message}
        # if data:
        #     res_dict = {'code': code, 'message': message, 'data': data}
        res_dict.update(kwargs)
        super().__init__(data=res_dict, *args, **kwargs)
