from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [

    path('post',views.post,name='post'),
    path('pros_cons/<int:id>',views.pros_cons,name='proscons'),
    path('comment/<int:id>',views.comment,name='comment'),

]

