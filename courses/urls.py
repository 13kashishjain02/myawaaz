from django.contrib import admin
from django.urls import path, include
from courses import views

urlpatterns = [

    path('', views.Subject_api),
    path('<int:id>/', views.Subject_api)

]