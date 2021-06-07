from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Contact
from datetime import date

# Create your views here.



def aboutus(request):
    # return render(request, "shop/index.html")
    return HttpResponse('aboutus')

