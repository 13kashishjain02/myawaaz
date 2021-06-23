from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from .models import Account
from django.contrib.auth.models import auth, User
from django.contrib.auth import logout, login, authenticate
from account.forms import AccountAuthenticationForm
import requests
import json
from django.http import HttpResponseRedirect, HttpResponse

# -----------------------------------------------------------------------

def userregister(request):
    msg=""
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        contact_number = request.POST['call']
        email = request.POST['email']
        organisation = request.POST['org']
        profession = request.POST['prof']
        gender = request.POST['gender']
        password = request.POST['password']
        try:
            user = Account.objects.create_user(
                firstname=firstname,lastname=lastname, email=email, organisation=organisation, profession=profession, gender=gender, password=password, contact_number=contact_number, viewpass=password
            )
            user.save()
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            msg = "User Registration Successful"
            # return render(request, 'account/register.html', {'msg': msg})
            return HttpResponse(msg)
        except IntegrityError as e:
            msg = email + " is already registered,if you think there is a issue please contact us at 6264843506"
            # return render(request, "account/register.html", {'msg': msg})
            return HttpResponse("is already registered,if you think there is a issue please contact us at 6264843506")
        except Exception as e:
            print("exception :",e)
        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        # return HttpResponse("registered")
        return render(request, 'account/signup.html')


def userlogin(request):
    msg = ""
    user = request.user
    if user.is_authenticated:
        return redirect("../")
    else:
        if request.POST:
            password = request.POST['password']
            email = request.POST['email']
            user= authenticate(email=email, password=password)
            if user:
                login(request, user)
                request.user = user
                next = request.POST.get('next', '../../')
                if next == "":
                    next="../../"
                return redirect(next)
                    # return redirect('../')
            else:
                msg = "invalid Email or password"
                print(msg)
        #     form = AccountAuthenticationForm(request.POST)
        #     if form.is_valid():
        #         email = form.cleaned_data['email']
        #         password = form.cleaned_data['password']
        #         user = authenticate(email=email, password=password)
        #         global usernamee
        #         usernamee = email
        #         if user:
        #             login(request, user)
        #             request.user = user
        #             next = request.POST.get('next', '../')
        #             if next == "":
        #                 next="../"
        #             return redirect(next)
        #             # return redirect('../')
        #         else:
        #             msg = "invalid Email or password"
        # else:
        #     form = AccountAuthenticationForm()

        return render(request, 'account/signin.html', { "msg": msg})
    # username=BaseUserManager.normalize_email(username)

    context['login form'] = form
    print("context :", context)
    return render(request, 'account/register.html', context)


@login_required(login_url="../login")
def logoutuser(request):
    logout(request)
    return redirect("../")


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
