from django.urls import path, re_path
from . import views
from . import models
app_name = 'infocards'

urlpatterns = [
    path('<int:shop_id>/settings/infocards',views.infocard,name="infocard"),
    path('<int:shop_id>/settings/menu/remove',views.menu_remove,name="menu_remove"),
    path('<int:shop_id>/settings/info',views.info,name="info"),    
    path('<int:shop_id>/settings/info_edit/<int:info_id>',views.info_edit,name="info_edit"),
    path('<int:shop_id>/settings/info_remove/<int:info_id>',views.info_remove,name="info_remove"),
]