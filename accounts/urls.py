from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/kakao/', views.Kakao_login, name = "kakao_signin"),
    path('signin/kakao/callback', views.Kakao_login_callback, name="kakao_signin_callback"),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('user_info/', views.user_info, name = "user_info"),    
    path('edit_info/<str:method>', views.edit_info, name = "edit_info"),    
]