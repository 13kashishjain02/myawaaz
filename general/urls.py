from django.urls import path,include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('index/',views.index,name='register'),
]

