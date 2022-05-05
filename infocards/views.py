from multiprocessing import context
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from shops.functions import *
from .forms import *
from .models import *
from shops.models import *
# Create your views here.

def infocard(request,shop_id):
    shop=get_shop(request,shop_id)
    infos = shop.category_set.all()
    if  request.POST.get("type") == "category" and request.method == 'POST':
        cat_form = CategoryRegisterForm(request.POST)
        cat_name = request.POST.get('name')
        if not Category.is_name(cat_name):
            messages.warning(request,f"{cat_name} 카테고리가 존재합니다.")
            return redirect('infocards:infocard',shop_id)
        if cat_form.is_valid():
            category = cat_form.save(commit=False)
            category.shop = shop
            category.save()     
            return redirect('infocards:infocard',shop_id)   
    else:
        cat_form = CategoryRegisterForm()
        
    if request.POST.get("type") == "menu" and request.method == 'POST':
        men_form = MenuRegisterForm(request.POST)
        men_name = request.POST.get('name')
        if not Menu.is_name(men_name):
            messages.warning(request,f"{men_name} 메뉴가 존재합니다.")
            return redirect('infocards:infocard',shop_id)
        if men_form.is_valid():
            menu = men_form.save(commit=False)
            menu.category = get_object_or_404(Category,id=request.POST.get('cat_id'))
            menu.content = request.POST.get('content')
            menu.price = request.POST.get('price')
            menu.save()
            return redirect('infocards:infocard',shop_id)
    else:
        men_form = MenuRegisterForm()
    context={'shop':shop,'men_form':men_form,'cat_form':cat_form,'infos':infos}
    return render(request,'infocards/infocards.html',context)


def menu_remove(request,shop_id):
    shop=get_shop(request,shop_id)
    if request.method == "POST":
        if request.POST.get('type')=='menu':
            menu = get_object_or_404(Menu,id=request.POST.get('men_id'))
            menu.delete()
            
        if request.POST.get('type')=='category':
            cat = get_object_or_404(Category,id=request.POST.get('cat_id'))
            cat.delete()
    context = {'shop':shop}
    return redirect('infocards:infocard',shop_id=shop_id)
    
@owner_required
def info(request,shop_id):
    shop = get_shop(request,shop_id)
    if request.method == "POST":
        info_form = InfoRegisterForm(request.POST,request.FILES)
        if info_form.is_valid():
            form = info_form.save(commit=False)
            form.shop = shop
            form.save()
            messages.success(request,"저장되었습니다.")
            return redirect('infocards:info',shop_id)
    else:
        info_form = InfoRegisterForm()
    context={'shop':shop,'form':info_form}
    return render(request,'infocards/setinfo.html',context)

@owner_required
def info_edit(request,shop_id,info_id):
    shop = get_shop(request,shop_id)
    info = get_object_or_404(Info,shop=shop,id=info_id)
    if request.method == "POST":
        info_form = InfoRegisterForm(request.POST,request.FILES,instance=info)
        if info_form.is_valid():
            form = info_form.save(commit=False)
            form.save()
            messages.success(request,"저장되었습니다.")
            return redirect('infocards:info',shop_id)
    else:
        info_form = InfoRegisterForm(instance=info)
    context={'shop':shop,'form':info_form}
    return render(request,'infocards/setinfo.html',context)
    
@owner_required
def info_remove(request,shop_id,info_id):
    shop=get_shop(request,shop_id)
    info = get_object_or_404(Info,shop=shop,id=info_id)
    info.delete()
    context = {'shop':shop}
    return redirect('infocards:info',shop_id)