from django.urls import path
from api.views import account
from api.views import topic
from api.views import news
from api.views import collect
from api.views import recommend
from api.views import comment

from rest_framework import routers

router = routers.SimpleRouter()
# 注册
router.register(r'register', account.RegView, 'register')
# 登录
# router.register(r'login', account.LoginView, 'login')
# 主题
router.register(r'topic', topic.TopicView, 'topic')
# 资讯
router.register(r'news', news.NewsView, 'news')
# 首页
router.register(r'zone', news.IndexView, 'zone')
# 收藏
router.register(r'collect', collect.CollectView, 'collect')
# 推荐
router.register(r'recommend', recommend.RecommendView, 'recommend')
# 评论
router.register(r'comment', comment.CommentView, 'comment')


urlpatterns = [
    # 登录
    path('login/', account.LoginView.as_view(), name='login')
]

urlpatterns += router.urls
