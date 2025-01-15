from django.contrib import admin
from django.urls import path , include
from . import views

from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.login),
    path('login',views.login , name='login'),
    path('get', views.get,name='get'),
    path('home', views.home,name='home'),
    path('logout', views.lo, name='logout'),
    path('emptyhome',views.emptyhome, name='emptyhome'),
]