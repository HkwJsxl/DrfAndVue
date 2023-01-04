"""自定义频率限制"""
import time
from rest_framework.throttling import BaseThrottle

# 访问频率限制次数
LIMIT_NUM = 3


class IPThrottle(BaseThrottle):
    # 定义成类属性,所有对象用的都是这个
    VISIT_DIC = {}

    def __init__(self):
        self.history_list = []

    def allow_request(self, request, view):
        """
        #（1）取出访问者ip
        #（2）如果当前ip不在访问字典里，添加进去，并且直接返回True,表示第一次访问，存在字典里，继续往下走
        #（3）循环判断当前ip的列表，有值，并且当前时间减去列表的最后一个时间大于60s，把这种数据pop掉，这样列表中只有60s以内的访问时间，
        #（4）判断，当列表小于3，说明一分钟以内访问不足三次，把当前时间插入到列表第一个位置，返回True，顺利通过
        #（5）当大于等于3，说明一分钟内访问超过三次，返回False验证失败
        """
        current_ip = request.META.get('REMOTE_ADDR')
        current_time = time.time()
        if current_ip not in self.VISIT_DIC:
            self.VISIT_DIC[current_ip] = [current_time]
            return True
        self.history_list = self.VISIT_DIC[current_ip]
        while True:
            if current_time - self.history_list[-1] > 60:
                self.history_list.pop(-1)
            else:
                break
        if len(self.history_list) < LIMIT_NUM:
            self.history_list.insert(0, current_time)
            return True
        else:
            return False

    def wait(self):
        """
        :return: 返回限制的剩余的秒数
        """
        last_time = self.history_list[-1]
        return 60 - (time.time() - last_time)
