from django.http import HttpResponse
from django.shortcuts import render
#
# Create your views here.#
def search_shops(request):
    #로직 예상도
    #카카오톡의 검색 결과를 받아온뒤
    #검색결과와 DB의 shop.roadAddr을 비교
    if request.method=="POST":
        pass
    return render(request,'clients/search.html')