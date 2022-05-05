from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render ,redirect
from django.contrib import messages
from django.http import HttpRequest,HttpResponse,JsonResponse
from shops.models import Shop
from waitings.models import Waiting
from .forms import *
from shops.functions import owner_required,active_required
from django.contrib.auth.decorators import login_required
# Create your views here.

@active_required
@login_required
def customer_views(request,shop_id):
    shop = Shop.objects.get(id=shop_id)
    context ={'shop':shop}
    return render(request,'waitings/views.html',context)

##매장 주인이 아닐시, 로그인 되어있으면 자동으로 자기 전화번호 입력.
@active_required
@login_required
def add_waiting(request,shop_id):        
    shop = Shop.objects.get(id=shop_id)
    phone_number = request.POST.get('phone_number')
    context= {'shop':shop,'phone_number':phone_number}
    # if not Shop.objects.filter(master=request.user,shop_id=shop_id):
    #     context += {'phone_number':request.user.phone_number}
    #     return render(request,'waitings/howmany.html',context)
    if request.method == 'POST':
        if Waiting.is_waiting(phone_number):
            messages.warning(request,f"이미 예약중입니다.")
            return render(request,'waitings/views.html',context)            
        if len(phone_number)<10:
            messages.warning(request,"전화번호가 너무 짧습니다.")
            return render(request,'waitings/views.html',context)            
        request.POST.adults = "0"
        request.POST.kids = "0"
        return render(request,'waitings/howmany.html',context)
    return render(request,'waitings/views.html',context)
@active_required
@login_required
def add_people(request,shop_id):    
    shop = Shop.objects.get(id=shop_id)
    _phone_number = request.POST.get('phone_number')
    adults = request.POST.get('adults')
    kids = request.POST.get('kids')
    if adults == "0" and kids == "0":
        context = {'phone_number':_phone_number,'shop':shop}
        return render(request,'waitings/howmany.html',context)
    how_many = int(adults)+int(kids)
    waiting = Waiting(phone_number=_phone_number,how_many=how_many,
            adults=adults,kids=kids,is_entered=False,
            shop_name=shop,is_disposed=False)
    #shop_id와 request.user가 일치하지 않으면 waiting.client=request.user
    if shop.master != request.user:
        waiting.client = request.user
    waiting.save()
    context = {'shop':shop}
    messages.success(request,"예약되었습니다.")
    return redirect('waitings:views',shop_id=shop.id)
    

def show_teams(request):
    shop_id = request.GET.get('shop_id')
    shop = Shop.objects.get(id=shop_id)
    waiting_list = Waiting.objects.filter(is_disposed=False,shop_name=shop)
    peoples = 0
    for i in waiting_list:
        peoples += i.how_many
    return JsonResponse({
        'resultCode': "S-1",
        'peoples' : str(peoples),
        'teams' : str(len(waiting_list)),
    })
    
@active_required
@login_required
def remote_waiting(request,shop_id):
    shop = get_object_or_404(Shop,id=shop_id)
    context={'shop':shop}
    return render(request,'waitings/remote.html',context)