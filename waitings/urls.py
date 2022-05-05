from django.urls import path, re_path
from . import views

app_name = 'waitings'
#
urlpatterns = [
    path('<int:shop_id>/views', views.customer_views, name = "views"),
    path('<int:shop_id>/add/waiting', views.add_waiting, name = "add_waiting"),
    path('<int:shop_id>/add/people', views.add_people, name = "add_people"),
    path('showteams/',views.show_teams,name="show_teams"),
    path('<int:shop_id>/add/remote',views.customer_views,name="remote")
]