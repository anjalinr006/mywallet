from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/wallet/', include('walletapi.urls')),

]
