from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from .functions import *
from waitings.models import *
from .models import *
from .form import *
from infocards.forms import *

@multiargs
def shop_register(request,*args,**kwargs):
    if request.method == 'POST':
        form = ShopRegisterForm(request.POST)  
        if form.is_valid():
            shop = form.save(commit=False)
            shop.master = request.user
            shop.save()
            Waiting.make_default(shop)
            context = {'method':'get'}
            return redirect('accounts:user_info')
    else:
        form = ShopRegisterForm()
    context = {'form':form}
    return render(request,'shops/register.html',context)

@multiargs
@owner_required
def shop_settings(request,*args,**kwargs):
    shop_id = kwargs['shop_id']
    shop=get_shop(request,shop_id)
    context={'shop':shop}
    return render(request,'shops/settings.html',context)

@owner_required
def shop_settings_location(request,shop_id):
    shop=get_shop(request,shop_id)
    if request.method == "POST":
        form = ShopRegisterForm(request.POST,instance=shop)
        name = request.POST.get('name')
        address = request.POST.get('address')
        if form.is_valid():
            if (name != '') and (address != ''):
                _shop = form.save(commit=False)
                _shop.save()
                messages.success(request,"수정되었습니다.")
                redirect('shops:location',shop_id)
    else:
        form = ShopRegisterForm(instance=shop)
    context={'shop':shop}
    return render(request,'shops/settings_location.html',context)

@owner_required
def shop_remove(request,shop_id):
    shops = Shop.objects.filter(master=request.user)
    context={'shops':shops}
    if request.method == "POST" and shop_id != 0:
        try:
            shop = get_object_or_404(Shop,master=request.user,id=shop_id)
            shop.delete()
            messages.warning(request,"삭제됨.")
            shops = Shop.objects.all()
            context={'shops':shops}
            return render(request,'shops:shop_delete',context)
        except:
            return redirect('search_main')
    return render(request,'shops/shop_delete.html',context)

@owner_required
def shop_admin_view(request,shop_id):
    shop=get_shop(request,shop_id)
    waitings_list = shop.waiting_set.all()
    context={'waitings_list':waitings_list,'shop':shop}
    return render(request,'shops/admin.html',context)

def get_waiting_list(request: HttpRequest):
    id = request.GET.get('from_id')
    shop_id = request.GET.get('shop_id')
    shop =get_shop(request,shop_id)
    _waiting_list = Waiting.objects.all().filter(id__gt=id,is_disposed=False,shop_name=shop).order_by('id')
    if _waiting_list.exists():
        waiting_list = list(_waiting_list.values())
    else:
        waiting_list = []
    return JsonResponse({
        'resultCode': "S-1",
        'waitings': waiting_list,
    })
    
@owner_required
def set_shop_status(request,shop_id):
    shop=get_shop(request,shop_id)
    shop.active = not shop.active
    shop.save()
    return redirect('accounts:user_info')
    
    
@owner_required
def remove_waiting(request):
    shop_id = request.GET.get('shop_id')
    message_id = request.GET.get('message_id')
    waiting = get_object_or_404(Waiting,id=message_id)
    waiting.delete_waiting()
    #카카오알림API로 취소 메세지 전송 구현해야함.
    #Waiting모델 메소드로 구현예정
    return redirect('shops:admin',shop_id=shop_id)

@owner_required
def call_waiting(request):
    shop_id = request.GET.get('shop_id')
    message_id = request.GET.get('message_id')
    whereami = len(Waiting.objects.filter(shop_name=shop_id,id__lt=message_id,is_entered=False,is_disposed=False))
    waiting = Waiting.objects.get(id=message_id)
    waiting.call_waiting(whereami)
    # Waiting모델의 메소드로 api콜 구현 예정
    # #카카오알림API로 취소 메세지 전송 구현해야함.
    # messages.success(request,f"{shop_id} : {message_id}")
    return redirect('shops:admin',shop_id=shop_id)

@owner_required
def enter_waiting(request):
    shop_id = request.GET.get('shop_id')
    message_id = request.GET.get('message_id')
    waiting = get_object_or_404(Waiting,id=message_id)
    waiting.enter_waiting()
    # waiting = Waiting.objects.get(id=message_id)
    # Waiting모델의 메소드로 api콜 구현 예정
    # #카카오알림API로 취소 메세지 전송 구현해야함.
    # messages.success(request,f"{shop_id} : {message_id}")
    return redirect('shops:admin',shop_id=shop_id)

def get_address(request):
    """
    도로명주소 검색 API서비스를 위한 함수입니다.
    """
    keyword = request.GET.get('keyword')
    page = request.GET.get('page')
    perPage = request.GET.get('perPage')
    locations = get_location(keyword,page,perPage)
    total_count = locations[-1]
    return JsonResponse({
        'resultCode': "S-1",
        'locations': locations[0],
        'total_count':total_count,
    })

def get_biznum(request):
    keyword = request.GET.get('keyword')
    biz_num,status = get_business_number(keyword)
    return JsonResponse({
        'resultCode': "S-1",
        'biz_num': biz_num,
        'status': status,
    })
    
def get_shops(request):
    """
    메인화면의 검색기능을 위한 함수입니다.
    """
    try:
        shop_name = request.GET.get('shop_name')
        page = int(request.GET.get('page'))
        perPage = int(request.GET.get('perPage'))
        shop_list=Shop.objects.filter(Q(name__icontains=shop_name)|Q(address__icontains=shop_name)).values()
        paginator = Paginator(shop_list,perPage)
        paged_shop_list = paginator.page(page)
        _shop = list(paged_shop_list)
        total_count = len(shop_list)
    except:
        return JsonResponse({
                'resultCode':"F-1",
                'shop':'',
                'shop_name':shop_name,
                'page':page,
                'perPage':perPage,
                'total_count':'0',
            })
    else:
        return JsonResponse({
            'resultCode':"S-1",
            'shop':_shop,
            'total_count':total_count,
        })
        
def filter_shop(request):
    """
    카카오맵에서 메인마커 주변에 위치한 매장의 정보를 받아오기 위한 함수입니다.
    """
    lat = float(request.GET.get('lat'))
    lng = float(request.GET.get('lng'))
    _range = float(request.GET.get('range'))
    range = _range**2*_range/800
    infos = []
    _shop = Shop.objects.filter(lat__gt=lat-range,lat__lt=lat+range,lng__gt=lng-range,lng__lt=lng+range)
    shop = list(_shop.values())
    for i in _shop:
        tmp = list(i.info_set.all().values())
        infos.append(tmp)
    
    return JsonResponse({
        'resultCode':"S-1",
        'shop':shop,
        'infos':infos,
        'range':range,
        'empty':'empty'
    })