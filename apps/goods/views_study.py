__author__ = 'zrc'
__date__ = '2019/6/6 15:38'

import json
from django.views import View
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,mixins,generics,viewsets,filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import GoodsSerializer,GoodsSerializerBase
from .models import Goods
from .filters import GoodsFilter


class GoodsListView(View):
    def get(self, request):
        goods = Goods.objects.all()[:5]

        # json_list = []
        # for good in goods:
        #     json_dict = dict()
        #     json_dict['name'] = good.name
        #     json_dict['price'] = good.price  # 日期没法序列化
        #     json_list.append(json_dict)

        # from django.forms.models import model_to_dict
        # json_list = []
        # for good in goods:
        #     json_dict = model_to_dict(good)  # ImageField 无法序列化
        #     json_list.append(json_dict)

        from django.core import serializers
        json_data = serializers.serialize('json', goods, ensure_ascii=False)

        # return HttpResponse(json.dumps(json_list, ensure_ascii=False), content_type='application/json,charset=utf-8')
        # return HttpResponse(json_data, content_type='application/json,charset=utf-8')
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii': False})


class GoodsListView2(APIView):
    """
    这是GoodsListView2的介绍ZRC
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:5]
        # serializer = GoodsSerializerBase(goods, many=True)
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # serializer = GoodsSerializerBase(data=request.data)
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodsListView3(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Goods.objects.all()[:5]
    serializer_class = GoodsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GoodsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListView4(generics.ListAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


class GoodsListViewSet1(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


class GoodsListViewSet3(viewsets.ModelViewSet):
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    def get_queryset(self):
        price_min = self.request.query_params.get("price_min", 100)
        return Goods.objects.filter(price__gte=price_min)


class GoodsListViewSet4(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'price')


class GoodsListViewSet5(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('^name', 'goods_desc')
    ordering_fields = ('price',)






