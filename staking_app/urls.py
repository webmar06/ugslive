
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from staking_app import views 

# from .views import load_new_user,load_points_table


urlpatterns = [
    # admin
    path('', views.home_stake,name='home_stake'),
    path('save_stake',views.save_stake,name='save_stake'),
    # ------mmmmmmmmm-------------- 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
