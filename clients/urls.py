from django.urls import path
from . import views
app_name="clients"

urlpatterns=[
    path('search/', views.search_shops, name = "search_shop"),    
]