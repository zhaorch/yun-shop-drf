from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import viewsets,status
from rest_framework import authentication,permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters,mixins
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin

from .models import Category,Goods
from .serializers import CategorySerializer,GoodsSerializer,UserSerializer
from .filters import GoodsFilter


# Create your views here.

User = get_user_model()

class ZRCPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.username == 'admin'

    def has_object_permission(self, request, view, obj):
        # 任何请求都允许读取权限，
        # 所以我们总是允许 GET，HEAD 或 OPTIONS 请求。
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        #return obj.id == request.user.id
        return True


class CommonPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        a = request.resolver_match.url_name
        return request.user.is_superuser == 1

    def has_object_permission(self, request, view, obj):
        # 任何请求都允许读取权限，
        # 所以我们总是允许 GET，HEAD 或 OPTIONS 请求。
        if request.method in permissions.SAFE_METHODS:
            return True
        #return obj.id == request.user.id
        return request.user.is_superuser == 1


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class CategoryViewSet(CacheResponseMixin,viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,ZRCPermission)

    queryset = Category.objects.all().filter(category_type = 1).order_by('-created_time')
    serializer_class = CategorySerializer


class GoodsViewSet(CacheResponseMixin,viewsets.ModelViewSet):
    #authentication_classes = (authentication.BasicAuthentication, authentication.SessionAuthentication,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication,)
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,CommonPermission)
    permission_classes = (permissions.IsAdminUser,)

    queryset = Goods.objects.all().order_by('category','-created_time').select_related('category')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_desc')
    ordering_fields = ('price',)

    # /goods/{pk}/detailInfo/
    @detail_route(methods=['get'])
    def detailInfo(self, request, pk=None):
        goods = get_object_or_404(Goods, pk=pk)
        result = {
            'name': goods.name,
            'price': goods.price
        }
        return Response(result, status=status.HTTP_200_OK)

    # /goods/goodsName/
    @list_route(methods=['get'],url_path='goodsName')
    def all_goods(self, request):
        music = Goods.objects.values_list('name', flat=True).distinct()
        return Response(music, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication,)
    permission_classes = (CommonPermission,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # /users/{pk}/userInfo/
    @detail_route(methods=['get'])
    def userInfo(self, request, pk=None):
        user =request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


