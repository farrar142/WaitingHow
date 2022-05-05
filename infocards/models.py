from django.db import models
from shops.models import Shop
# Create your models here.
class Info(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    image = models.ImageField('소개사진',upload_to="infos/info/%Y/%m/%d",blank=True,null=True)
    content = models.TextField('소개글')
    
class Category(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField('매장이름',max_length=100)
    @classmethod  
    def is_name(cls,cat_name):
        try:
            Category.objects.get(name=cat_name)
            return False
        except:
            return True
    
    def __str__(self):
        return f"{self.name}"
    
class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField('메뉴사진',upload_to="infos/menu/%Y/%m/%d",blank=True,null=True)
    name = models.CharField('메뉴이름',max_length=100)
    content = models.CharField('메뉴설명',max_length=100,blank=True,null=True)
    price = models.PositiveIntegerField('메뉴가격')
    @classmethod  
    def is_name(cls,men_name):
        try:
            Menu.objects.get(name=men_name)
            return False
        except:
            return True
    def __str__(self):
        return f"{self.name}"