__author__ = 'zrc'
__date__ = '2019/6/4 8:28'

from rest_framework import serializers
from DjangoUeditor.models import UEditorField
from django.db.models import Q
from django.contrib.auth.models import AbstractUser

from .models import Category, Goods


class CategorySerializerName(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')


class CategorySerializer2(serializers.ModelSerializer):
    category_type = serializers.CharField(source='get_category_type_display')
    pid = CategorySerializerName()
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Category
        #fields = ('name', 'url',"category_type", "pid")
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    category_type = serializers.CharField(source='get_category_type_display')
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    # goods = serializers.SerializerMethodField()
    #
    # def get_goods(self, obj):
    #     all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__pid_id=obj.id))
    #     goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
    #     return goods_serializer.data

    class Meta:
        model = Category
        #fields = ('name', 'url',"category_type", "pid",'sub_cat')
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializerName()
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Goods
        fields = "__all__"


class GoodsSerializerBase(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    category = serializers.CharField()
    price = serializers.FloatField(default=0)
    goods_desc = serializers.CharField()
    goods_front_image = serializers.ImageField()
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def create(self, validated_data):
        return Goods.objects.create(**validated_data)


from django.contrib.auth import get_user_model
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email')


class GoodsSerializerExtension(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Goods
        fields = "__all__"