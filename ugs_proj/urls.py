
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staking/',include('staking_app.urls')),
    path('',include('ugs_app.urls')),
    
]
