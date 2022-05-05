from django.db import models
from accounts.models import User
# Create your models here.

class Shop(models.Model):
    master = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('매장이름',max_length=100)
    bizNum=models.CharField('사업자등록번호',max_length=20,blank=True,null=True)
    zipNo = models.CharField('우편번호',max_length=10)
    address = models.CharField('매장위치',max_length=200)
    detailAddress = models.CharField('상세주소',max_length=200)
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    lat = models.CharField('위도',max_length=30)
    lng = models.CharField('경도',max_length=30)
    active = models.BooleanField(default=False)
    
    @classmethod
    def is_bizNum(cls,bizNum):
        try:
            shop = Shop.objects.get(bizNum=bizNum)
            return True
        except:
            return False
        
    def is_active(self):
        return self.active

    def __str__(self):
        return f"{self.name}"