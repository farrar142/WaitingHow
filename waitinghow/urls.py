from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from accounts import views as accounts_views
from shops import views as shop_views
from clients import views as clients_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('shops/', include('shops.urls')),
    path('waitings/', include('waitings.urls')),
    path('clients/', include('clients.urls')),
    path('infocards/', include('infocards.urls')),
    path('',clients_views.search_shops,name='search_main'),
    path('user_info',clients_views.search_shops,name='user_info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)