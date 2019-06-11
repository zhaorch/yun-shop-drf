__author__ = 'zrc'
__date__ = '2019/6/4 9:19'

import django_filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    name = django_filters.CharFilter(field_name='name', help_text="名称", lookup_expr='contains')
    pricemin = django_filters.NumberFilter(field_name='price', help_text="最低价格",lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='price', help_text="最高价格", lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter', help_text="分类")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value)|Q(category__pid_id=value))

    class Meta:
        model = Goods
        fields = ['name','pricemin', 'pricemax']