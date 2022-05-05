from django.urls import path, re_path
from . import views
app_name = 'shops'

urlpatterns = [
    path('register/', views.shop_register, name = "register"),
    path('<int:shop_id>/',views.shop_admin_view,name="admin"),
    path('<int:shop_id>/settings/',views.shop_settings,name="settings"),
    path('<int:shop_id>/status/',views.set_shop_status,name="status"),
    
    
    path('<int:shop_id>/settings/location',views.shop_settings_location,name="location"),
    
    path('<int:shop_id>/remove/',views.shop_remove,name="shop_remove"),    
    path('render_list/',views.get_waiting_list,name='get_waiting_list'),
    path('remove',views.remove_waiting,name='remove'),
    path('call',views.call_waiting,name='call'),
    path('enter',views.enter_waiting,name='enter'),
    path('get_shops/',views.get_shops,name='get_shops'),
    path('get_address/',views.get_address,name='get_address'),
    path('get_biznum/',views.get_biznum,name='get_biznum'),
    path('filtered_shop',views.filter_shop,name='filter'),
    
    
    path('test',views.test,name='test'),
]