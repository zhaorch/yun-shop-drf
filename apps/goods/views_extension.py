__author__ = 'zrc'
__date__ = '2019/6/25 17:40'

from rest_framework_extensions.mixins import DetailSerializerMixin
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets,authentication,permissions,filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.mixins import PaginateByMaxMixin

from .models import Category,Goods
from .serializers import CategorySerializer,GoodsSerializer,GoodsSerializerExtension,UserSerializer
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


# 正式情况加上缓存
# class GoodsViewSet2(CacheResponseMixin,PaginateByMaxMixin, DetailSerializerMixin, viewsets.ModelViewSet):
class GoodsViewSet2(PaginateByMaxMixin,DetailSerializerMixin, viewsets.ModelViewSet):
    #authentication_classes = (authentication.BasicAuthentication, authentication.SessionAuthentication,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication,)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,CommonPermission)
    permission_classes = (permissions.IsAdminUser,)

    queryset = Goods.objects.all().order_by('category','-created_time')
    serializer_class = GoodsSerializerExtension

    queryset_detail = queryset.select_related('category')
    serializer_detail_class = GoodsSerializer

    pagination_class = GoodsPagination

    # 这个貌似不起作用。。不搞了 page_size=max
    max_paginate_by = 100

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_desc')
    ordering_fields = ('price',)