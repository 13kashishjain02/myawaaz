from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from .models import Account, VendorAccount, BloggerAccount
from django.contrib.auth.models import auth, User
from django.contrib.auth import logout, login, authenticate
from account.forms import AccountAuthenticationForm
import requests
import json
from datetime import date
from django.core.files.storage import default_storage
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect, HttpResponse
# ---------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------



# -----------------------------------------------------------------------

def userregister(request):
    msg=""
    if request.method == 'POST':
        name = request.POST['name']
        contact_number = int(request.POST['contact_number'])
        email = request.POST['email']
        password = request.POST.get('password')
        try:
            user = Account.objects.create_customer(
                name=name, email=email, password=password, contact_number=contact_number, viewpass=password
            )
            user.save()
            login(request, user)
            msg = "User Registration Successful"
            return render(request, 'account/register.html', {'msg': msg})
        except IntegrityError as e:
            msg = email + " is already registered,if you think there is a issue please contact us at 6264843506"
            return render(request, "account/register.html", {'msg': msg})
        except Exception as e:
            print("exception :",e)
        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return render(request, "account/register.html", {'msg': msg})


def userlogin(request):
    msg = ""
    user = request.user
    if user.is_authenticated:
        return redirect("../")
    else:
        if request.POST:
            form = AccountAuthenticationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(email=email, password=password)
                global usernamee
                usernamee = email
                if user:
                    login(request, user)
                    request.user = user
                    next = request.POST.get('next', '../')
                    if next == "":
                        next="../"
                    return redirect(next)
                    # return redirect('../')
                else:
                    msg = "invalid Email or password"
        else:
            form = AccountAuthenticationForm()
        return render(request, 'account/login.html', {"form": form, "msg": msg})
    # username=BaseUserManager.normalize_email(username)

    context['login form'] = form
    print("context :", context)
    return render(request, 'account/register.html', context)


@login_required(login_url="../login")
def logoutuser(request):
    logout(request)
    return redirect("../")


@login_required(login_url="../login")
def vendorregister(request):
    global shopname
    global shop_add
    global plan
    global vendorname
    global vendoremail
    global mobile
    global promocode
    global gst

    if request.method == 'POST':
        email = request.user.email
        shop_number = request.POST.get('shop_number')
        shopname = request.POST.get('shopname').lower()
        gst = request.POST.get('gst')
        shop_add_flat = request.POST['shop_add_flat']
        shop_add_city = request.POST['shop_add_city']
        shop_add_state = request.POST['shop_add_state']
        shop_add_pincode = str(request.POST.get('shop_add_pincode'))
        # shop_add = shop_add_flat + "," + shop_add_city + "," + shop_add_state + "," + shop_add_pincode
        plan = request.POST['plan']
        subscription_amount = 50
        vendor = Account.objects.get(email=email)
        vendor.is_Vendor = True
        vendor.save()
        promocode = request.POST.get('promocode')

        try:
            user = VendorAccount.objects.create(
                shop_name=shopname, shop_number=shop_number, shop_add=shop_add_flat, city=shop_add_city,
                state=shop_add_state, plan=plan, gst=gst, vendor=vendor,
                subscripton_amount=subscription_amount, email=email)
            user.save()

        except IntegrityError as e:
            e = str(e)
            if e == "UNIQUE constraint failed: account_vendoraccount.shop_name":
                shopname = shopname + "#" + vendor.name[2:5]

                user = VendorAccount.objects.create(
                    shop_name=shopname, shop_number=shop_number, shop_add=shop_add, plan=plan, gst=gst, vendor=vendor,
                    subscripton_amount=subscription_amount, email=email)
                user.save()
            else:
                msg = "vendor already registered,if you think there is a issue please contact us at 6264843506"
                return render(request, "account/vendorregister.html", {'msg': msg})

        # twilio message
        # account_sid = 'AC58aae686ada0a42728e123cfee24cd5b'
        # auth_token = '1d2bfa8c3b98e92dd3d9c271fba9463e'
        # client = Client(account_sid, auth_token)
        #
        # message = client.messages \
        #     .create(
        #     body="a new vendor has registored, email=" + email + "shopname =" + shopname + "and contact_number is " + str(
        #         mobile),
        #     from_='+14159696324',
        #     to='+916264843506'
        # )

        # print(message.sid)

        # return redirect("../subscription")
        msg = "Vendor Registration Successful"
        return render(request, 'general/index.html', {'msg': msg})
    else:
        return render(request, "account/vendorregister.html")


@login_required(login_url="../login")
def bloggerregister(request):
    if request.method == 'POST':
        email = request.user.email
        blogname = request.POST['blogname'].lower()
        bio = request.POST.get('bio')
        shop_add_flat = request.POST['shop_add_flat']
        shop_add_city = request.POST['shop_add_city']
        shop_add_state = request.POST['shop_add_state']
        shop_add_pincode = str(request.POST.get('shop_add_pincode'))
        # shop_add = shop_add_flat + "," + shop_add_city + "," + shop_add_state + "," + shop_add_pincode
        plan = request.POST.get('plan')
        subscription_amount = 50
        blogger = Account.objects.get(email=email)
        blogger.is_Blogger = True
        blogger.save()
        promocode = request.POST.get('promocode')
        print("here")
        try:
            print("here")
            user = BloggerAccount.objects.create(
                blogname=blogname, address=shop_add_flat, city=shop_add_city,
                state=shop_add_state, plan=plan, blogger=blogger,
                subscripton_amount=subscription_amount, email=email)
            user.save()
            print("here save successfull")

        except IntegrityError as e:
            e = str(e)
            print("here")
            print(e)
            if e == "UNIQUE constraint failed: account_bloggeraccount.blogname":
                blogname = blogname + "#" + blogger.name[2:5]

                user = BloggerAccount.objects.create(
                    blogname=blogname, address=shop_add_flat, city=shop_add_city,
                    state=shop_add_state, plan=plan, blogger=blogger,
                    subscripton_amount=subscription_amount, email=email)
                user.save()
            else:
                msg = "vendor already registered,if you think there is a issue please contact us at 6264843506"
                return render(request, "account/blogger_registeration.html", {'msg': msg})

        # twilio message
        # account_sid = 'AC58aae686ada0a42728e123cfee24cd5b'
        # auth_token = '1d2bfa8c3b98e92dd3d9c271fba9463e'
        # client = Client(account_sid, auth_token)
        #
        # message = client.messages \
        #     .create(
        #     body="a new vendor has registored, email=" + email + "shopname =" + shopname + "and contact_number is " + str(
        #         mobile),
        #     from_='+14159696324',
        #     to='+916264843506'
        # )

        # print(message.sid)

        # return redirect("../subscription")
        return redirect("../")
    else:
        return render(request, "account/blogger_registeration.html")


@login_required(login_url="../login")
def account_view(request):
    # if not request.user.is_authenticated:
    #     return redirect("../login")
    msg=""
    context = {"name": request.user.name, "email": request.user.email, "contact_number": request.user.contact_number,
               "msg": msg}
    if request.POST:
        name = request.POST['name']
        contact_number = request.POST.get('contact_number')
        email = request.POST['email']
        password = request.POST.get('password')
        user = authenticate(email=request.user.email, password=password)
        if user:
            userid = request.user.id
            Account.objects.filter(id=userid).update(name=name, email=email, contact_number=contact_number)
            context = {"name": name, "email": email, "contact_number": contact_number, "msg": ""}
        else:
            msg = "Wrong Password"
            context["msg"] = msg
    return render(request, 'account/myaccount.html', context)


@login_required(login_url="../login")
def changepassword(request):
    msg=""
    password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    user = authenticate(email=request.user.email, password=password)
    if user:
        if new_password == confirm_password:
            userid = request.user.id
            u = Account.objects.get(id=userid)
            u.set_password(new_password)
            u.save()
            Account.objects.filter(id=userid).update(viewpass=new_password, )
            msg = "Password Changed"
        else:
            msg = "new password does not match with confirm password"
    else:
        msg = "Wrong password"
    return redirect("../account")
