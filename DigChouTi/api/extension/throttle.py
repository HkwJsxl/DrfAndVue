from rest_framework.throttling import SimpleRateThrottle
from rest_framework import exceptions
from rest_framework import status
from django.core.cache import cache as default_cache

from api.extension import return_code


class ThrottledException(exceptions.APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 'throttled'


class NewsRateThrottle(SimpleRateThrottle):
    cache = default_cache  # 访问记录存放在django的缓存中（需设置缓存）
    scope = 'user_access'  # 构造缓存中的key
    cache_format = 'throttle_%(scope)s_%(ident)s'
    # 设置访问频率, 's', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day'
    THROTTLE_RATES = {scope: '1/5m'}
    # THROTTLE_RATES = {scope: '1/5s'}

    def get_cache_key(self, request, view):
        ident = request.user.pk  # 用户ID
        return self.cache_format % {'scope': self.scope, 'ident': ident}

    def throttle_failure(self):
        wait = self.wait()
        detail = {
            'status': return_code.TOO_MANY_REQUESTS,
            'message': '访问频率限制',
            'detail': '需等待{}s才能访问'.format(int(wait))
        }
        raise ThrottledException(detail)

    def parse_rate(self, rate):
        """重写：五分钟1次限制"""
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[-1]]
        count = int(period[0:-1])
        return num_requests, count * duration

    def throttle_success(self):
        # self.history.insert(0, self.now)
        # self.cache.set(self.key, self.history, self.duration)
        return True

    def done(self):
        """数据插入成功后在执行这个方法"""
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
