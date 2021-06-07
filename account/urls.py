from django.urls import path,include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',views.userregister,name='register'),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('account/',views.account_view,name='account'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('social-auth/', include('social_django.urls', namespace="social")),
]

