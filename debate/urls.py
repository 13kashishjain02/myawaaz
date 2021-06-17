from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [

    path('',views.index,name='home'),
    path('post',views.post,name='post'),
    path('pros_cons/<int:id>',views.pros_cons,name='proscons'),
    path('comment/<int:id>',views.comment,name='comment'),
    path('comment-api/<int:id>',views.comment_api,name='comment_api'),
    path('comment-api/',views.comment_api,name='comment_api'),
    path('addpros/<int:id>',views.add_pros,name='add_pros'),
    path('addcons/<int:id>', views.add_cons, name='add_cons'),
    path('<slug:slug>',views.post_view,name='view'),
]

