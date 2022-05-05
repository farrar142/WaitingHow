import json
import requests
import os
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlcleanup, urlopen
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.db.models import Count
from .models import *
#


def multiargs(cb, *_args, **_kwargs):
    def wrap(request, *args, **kwargs):
        test = os.environ.get("DJANGO_SETTINGS_MODULE")
        # if test == "waitinghow.settings":
        # messages.success(request,test)
        # messages.success(request,request.GET)
        # messages.success(request,request.POST)
        # messages.success(request,request)
        # messages.success(request,args)
        # messages.success(request,kwargs)
        return cb(request, *args, **kwargs)
    return wrap


def owner_required(func):
    def wrapper(request, *args, **kwargs):
        try:
            shop_id = request.GET.get('shop_id') or kwargs['shop_id']
            if shop_id == 0:
                return func(request, *args, **kwargs)
            Shop.objects.get(master=request.user, id=shop_id)
            return func(request, *args, **kwargs)
        except:
            messages.warning(request, f"권한이 없습니다.")
            return redirect("search_main")
    return wrapper


def active_required(func):
    def wrapper(request, *args, **kwargs):
        try:
            shop_id = request.GET.get('shop_id') or kwargs['shop_id']
            if shop_id == 0:
                return func(request, *args, **kwargs)
            shop = Shop.objects.get(id=shop_id)
            if shop.active:
                return func(request, *args, **kwargs)
            else:
                raise
        except:
            messages.warning(request, f"영업중이 아닙니다.")
            return redirect("search_main")
    return wrapper


def get_shop(request, shop_id):
    return Shop.objects.get(master=request.user, id=shop_id)


def get_location(keyword, page=1, perPage=5):
    """
    keyword,page,perPage
    """
    print('도로명주소 검색API 서비스를 이용한 주소검색결과를 보여줍니다.')
    keystr = keyword
    # print(resulttype)
    url = 'http://www.juso.go.kr/addrlink/addrLinkApi.do?'
    queryParams = urlencode({
        quote_plus('currentPage'): page,
        quote_plus('countPerPage'): perPage,
        quote_plus('resultType'): 'json',
        quote_plus('keyword'): keystr,
        quote_plus('confmKey'): 'bGk3MHZtMWJ2anNkODIwMTQwOTEyMTg0NDI2'})
    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    # print(response_body.decode('utf-8'))
    root_json = json.loads(response_body)
    return root_json['results']['juso'], root_json['results']['common']['totalCount']


def get_business_number(keyword, page=1):
    keyword = ''.join(char for char in keyword if char.isnumeric())
    print('사업자등록번호 진위확인 결과')
    # print(resulttype)
    servicekey = "nrLkreVR2m5/tpeX8mR+UDErIofoRGze1evKCsyWB1GlktVcTpcaeXaFcOYJ/mqnse5aTn1+WpyH5BkPixJOhw=="
    datas = json.dumps({
        "b_no": [keyword],
    })
    url = "https://api.odcloud.kr/api/nts-businessman/v1/status?" + urlencode({
        quote_plus('serviceKey'): servicekey
    })
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    results = requests.post(url, data=datas, headers=headers).json()
    if results['data'][0]['b_stt_cd'] != '':
        status = True
    else:
        status = False
    return keyword, status


gbShop = {}


def test(request):
    global gbShop
    if not gbShop:
        gbShops = Shop.objects.all()
        ami = "no"
    else:
        ami = "yes"
    _result = gbShops.filter(id=1)
    result = list(_result.values())
    return JsonResponse({
        'resultCode': "S-1",
        'result': result,
        'ami': ami,
    })
