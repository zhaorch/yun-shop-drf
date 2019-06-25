"""YunShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import xadmin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from YunShop.settings import MEDIA_ROOT
from goods.views import CategoryViewSet, GoodsViewSet, UserViewSet
from goods.views_study import GoodsListView1, GoodsListView2, GoodsListView3,GoodsListView4
from goods.views_study import GoodsListViewSet1,GoodsListViewSet3,GoodsListViewSet4,GoodsListViewSet5
from goods.views_extension import GoodsViewSet2

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'category', CategoryViewSet, 'category')
router.register(r'goods', GoodsViewSet, 'goods')
router.register(r'study/goodsViewSet2', GoodsListViewSet1, 'study_goodsViewSet2')
router.register(r'study/goodsViewSet3', GoodsListViewSet3, 'study_goodsViewSet3')
router.register(r'study/goodsViewSet4', GoodsListViewSet4, 'study_goodsViewSet4')
router.register(r'study/goodsViewSet5', GoodsListViewSet5, 'study_goodsViewSet5')

router.register('goods-extension', GoodsViewSet2, 'goods-extension')


study_goods = GoodsListViewSet1.as_view({
    'get': 'list'
})

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    re_path(r'^ueditor/', include('DjangoUeditor.urls')),

    re_path(r'docs/', include_docs_urls(title="渣渣网")),

    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # JWF 认证接口
    path(r'login/', obtain_jwt_token),

    path('', include(router.urls)),

    # 学习
    path('study/goods1', GoodsListView1.as_view(), name='goods-list'),
    path('study/goods2', GoodsListView2.as_view(), name='goods-list2'),
    path('study/goods3', GoodsListView3.as_view(), name='goods-list3'),
    path('study/goods4', GoodsListView4.as_view(), name='goods-list4'),
    path('study/goodsViewSet', study_goods, name='goods-list5'),
]
