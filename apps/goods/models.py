import datetime
from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.


class Category(models.Model):
    """
        商品类别
        """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别", help_text="类别名")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="级别", help_text="类目级别")
    pid = models.ForeignKey("self", null=True, blank=True, verbose_name="父类别", help_text="父目录", related_name="sub_cat", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=100, verbose_name="商品名")
    category = models.ForeignKey(Category, verbose_name="商品类目",null=True,blank=True, on_delete=models.SET_NULL)
    price = models.FloatField(default=0, verbose_name="价格")
    goods_desc = UEditorField(verbose_name="内容", width=1000, height=400, toolbars="full", imagePath="goods/ueditor/",
                        filePath="goods/ueditor/",default='')
    goods_front_image = models.ImageField(upload_to="goods/images/%Y/%m", null=True, blank=True, verbose_name="封面图")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name