from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home),
    path('signup',views.signuppage , name='signup')
]