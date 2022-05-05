from django.shortcuts import render,redirect, resolve_url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpRequest
from django.contrib import messages
from accounts.models import *
from shops.models import Shop
from waitings.models import Waiting
from .models import *
import requests,os

# Create your views here.
def user_info(request):
    user = request.user
    context={}
    if user.is_authenticated:
        ##유저가 가지고있는 waitings의 id값을 가져옴.
        ## waitings가 가지고 있는 shop의 waitings에서 id값보다 낮은 객체들 필터
        waitings = request.user.waitings_set.filter(is_disposed=False)
        #waiting = waitings.first()
        #shop_waiting = waiting.shop_name.waiting_set.filter(id__lt = waiting.id,is_disposed=False).count()
        context.update({'waitings':waitings})
        if user.have_shop:
            shops_list = Shop.objects.filter(master=user)
            context.update({'shops_list': shops_list})
            return render(request,'accounts/user_info.html',context)
        return render(request,'accounts/user_info.html',context)
    else:
        messages.success(request,"로그인실패")
        return render(request,'accounts/user_main.html')
    
def Kakao_login(request : HttpRequest):
    REST_API_KEY = os.environ.get("WAITING_HOW__REST_API_KEY")
    REDIRECT_URI = os.environ.get("WAITING_HOW__LOGIN_REDIRECT_URI")
    next_url = request.GET.get('next')
    kakao_auth_api = "https://kauth.kakao.com/oauth/authorize?"
    return redirect(
        f"{kakao_auth_api}client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&state={next_url}"
    )
def Kakao_login_callback(request):
    code = request.GET.get("code")
    REST_API_KEY = os.environ.get("WAITING_HOW__REST_API_KEY")
    REDIRECT_URI = os.environ.get("WAITING_HOW__LOGIN_REDIRECT_URI")
    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
    )

    token_json = token_request.json()

    error = token_json.get("error", None)
    if error is not None:
        raise Exception('카카오 로그인 에러')

    access_token = token_json.get("access_token")

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()

    id = profile_json.get("id")

    User.login_with_kakao(request, id)
    user = User.objects.get(provider_accounts_id=id)
    messages.success(request, f"{user.username}님 카카오톡 계정으로 로그인되었습니다")
    next_url = request.GET.get('state')
    if next_url.lower() != "none":
        return redirect(next_url)
    return redirect("accounts:user_info")

def edit_info(request,method):
    if method == "POST":
        pass
    elif method == "GET":
        return render(request,'accounts/edit_info.html')