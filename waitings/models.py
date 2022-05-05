from django.db import models
from django.shortcuts import render, get_object_or_404
from django.core.validators import MaxValueValidator
from django.contrib import messages
from shops.models import Shop
from solapi.send_sms import send_message
# Create your models here.


class Waiting(models.Model):
    phone_number = models.CharField('전화번호',max_length=12)
    how_many = models.PositiveIntegerField('예약인수',null=True)
    adults = models.PositiveIntegerField('성인',null=True)
    kids = models.PositiveIntegerField('유아',null=True)
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    is_entered = models.BooleanField('입장여부')
    is_disposed = models.BooleanField('처리여부')
    shop_name = models.ForeignKey(Shop,on_delete=models.CASCADE)
    client = models.ForeignKey('accounts.User',on_delete=models.CASCADE,null=True,blank=True,related_name="waitings_set")
    is_called = models.BooleanField('호출여부',default=False,null=True,blank=True)
    @classmethod
    def make_default(cls,shop):
        Waiting(phone_number=0,how_many=0,adults=0,kids=0,is_entered=False,shop_name=shop,is_disposed=True).save()
    @classmethod
    def is_waiting(cls,phone_number):
        try:
            waiting = Waiting.objects.get(phone_number=phone_number,is_disposed=False)
            return True
        except:
            return False
    @classmethod
    def show_phone_number(cls,phone_number):
        qoute = '-'
        if len(phone_number)==11:
            result = phone_number[0:3]+qoute+phone_number[3:7]+qoute+phone_number[7:11]
        if len(phone_number)==10:
            result = phone_number[0:3]+qoute+phone_number[3:6]+qoute+phone_number[6:10]
        return result
    def delete_waiting(self):
        '''
        phone_number에 적힌 번호를 기준으로 카카오톡 알림api호출
        '''
        self.is_entered = False
        self.is_disposed = True
        self.save()
    def enter_waiting(self):
        '''
        phone_number에 적힌 번호를 기준으로 카카오톡 알림api호출
        '''
        self.is_entered = True
        self.is_disposed = True
        self.save()
    def call_waiting(self,number):
        '''
        phone_number에 적힌 번호를 기준으로 카카오톡 알림api호출
        '''
        context = f"{self.shop_name}의 대기열이 {number}팀 남았습니다."
        if "000" not in self.phone_number:
            send_message(self.phone_number,context)
        self.is_called = True
        self.save()