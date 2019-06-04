__author__ = 'zrc'
__date__ = '2019/6/3 18:37'

import xadmin
from .models import Goods, Category

class GoodsAdmin(object):
    list_display = ["name", "price","category","goods_desc", "created_time"]
    search_fields = ['name', ]
    list_editable = ["price", ]
    list_filter = ["name","price", "category__name"]
    style_fields = {"goods_desc": "ueditor"}


class CategoryAdmin(object):
    list_display = ["name", "category_type", "pid", "created_time"]
    list_filter = ["category_type", "pid", "name"]
    search_fields = ['name', ]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(Category, CategoryAdmin)