__author__ = 'zrc'
__date__ = '2019/6/6 15:38'

import json
from django.views import View
from django.http import HttpResponse,JsonResponse


from .models import Goods


class GoodsListView(View):
    def get(self,request):
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

        #return HttpResponse(json.dumps(json_list, ensure_ascii=False), content_type='application/json,charset=utf-8')
        #return HttpResponse(json_data, content_type='application/json,charset=utf-8')
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii': False})