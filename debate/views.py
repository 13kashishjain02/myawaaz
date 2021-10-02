from django.shortcuts import render, redirect
from django.db.models import Count
from debate.models import Debate,Pros,Cons
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import DebateSerializer,ProsCommentSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import re

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.title.lower():
        return True
    else:
        return False

def index(request):
    debate=Debate.objects.all()
    for i in debate:
        i.likecount=i.like.count()
    return render(request,"debate/index.html",{"debate":debate})

def explore(request):
    debate=Debate.objects.annotate(q_count=Count('like')).order_by('-q_count')
    for i in debate:
        i.likecount=i.like.count()
    return render(request,"debate/explore.html",{"debate":debate})

def tag_filter(request,tag):
    debate=Debate.objects.annotate(q_count=Count('like')).order_by('-q_count').filter(tags=tag)
    # debate=debate.objects.filter(tags=tag)
    for i in debate:
        i.likecount=i.like.count()
    return render(request,"debate/tags_filter.html",{"debate":debate})

def post_view(request,slug):
    debate = Debate.objects.get(slug=slug)
    pros=Pros.objects.filter(debate_pros=debate)
    cons = Cons.objects.filter(debate_cons=debate)
    # return HttpResponse(slug)
    debate.likecount = debate.like.count()
    if debate.tags:
        # debate.tags=debate.tags.split(",")
        debate.tags=re.split('; |,| |\n', debate.tags)

    for i in pros:
        i.likecount=i.proslike.count()
        if i.pros_tags:
            i.tags=i.pros_tags.split(" ")

    for i in cons:
        i.likecount=i.conslike.count()
        if i.cons_tags:
            i.tags=i.cons_tags.split(" ")
    return render(request, "debate/post_page.html", {"debate": debate,"pros":pros,"cons":cons})

def post(request):
    if request.method == 'POST':
        try:
            title=request.POST['title']
            slug = title.replace(" ", "-")
            debate=Debate.objects.create(title=title,slug=slug)
            debate.save()
        except IntegrityError as e:
            msg = "discussion with this title already exist"
            return HttpResponse(msg)
        return HttpResponse("done")
    else:
        return render(request, "debate/add-discussion.html")

def pros_cons(request,id):
    # Debate.objects.filter(data__owner__other_pets__0__name='Fishy')
    debate=Debate.objects.get(id=id)

    #section takes the value pros & cons depending on where the user posted his views
    section="pros"

    #his view; what he posted is saved by post
    post="point 4"

    if section=="pros":
        debate.pros['pros'].append({'pros': post})
        debate.save()
    else:
        debate.cons['cons'].append({'cons': post})
        debate.save()
    return HttpResponse("done")

@login_required(login_url="../../login")
def comment(request):
    section = request.GET.get("section")
    id= request.GET.get("id")

    # his view; what he commented is saved by comment
    comment = request.GET.get("comment")
    user=request.user
    # name=user.firstname+" " +user.lastname
    email=user.email
    if section == "pros":
        pros = Pros.objects.get(id=id)
        pros.comment.append({"comment":comment,"email":email})
        pros.save()
    else:
        cons = Cons.objects.get(id=id)
        cons.comment.append({"comment": comment, "email": email})
        cons.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def add_pros(request,id):
    debate = Debate.objects.get(id=id)
    if request.method=='POST':
        point=request.POST['pro']
        tags = request.POST['tags']
        pros = Pros.objects.create(debate_pros=debate,pros=point,pros_tags=tags)
        pros.save()
    url="../" + debate.slug+"!"
    return redirect(url)

def add_cons(request,id):
    debate = Debate.objects.get(id=id)
    if request.method == 'POST':
        point = request.POST['con']
        tags = request.POST['tags']
        cons = Cons.objects.create(debate_cons=debate,cons=point,cons_tags=tags)
        cons.save()
    url = "../" + debate.slug + "!"
    return redirect(url)

@csrf_exempt
@api_view(['POST','GET',])
def comment_api(request,id=None):
    if request.method=="GET":
        if id is None:
            data=Pros.objects.all()
            serializer=ProsCommentSerializer(data,many=True)
            return Response(serializer.data)

        else:
            # debate=Debate.objects.get(pk=id)
            data=Pros.objects.filter(pk=id)
            serializer=ProsCommentSerializer(data,many=True)
            return Response(serializer.data)


    if request.method=='POST':
        serializer=ProsCommentSerializer(data=request.data)
        # print(serializer.data)
        if serializer.is_valid():
            comment=serializer.data
            data = Pros.objects.get(pk=id)
            print(comment)
            user=request.user
            try:
                name=user.firstname + " "+ user.lastname
            except:
                name="annonymous"

            comment["name"]=name
            comment["email"] = user.email
            print(comment["comment"])
            # request in form
            # {
            #     "comments":
            #         {
            #             "name": "ram",
            #             "comment": "jai shree ram"
            #         }
            # }

            data.comment.append(comment)
            data.save()

            # serializer.save()
            return Response({'msg','DATA CREATED'})
        return Response(serializer.errors)

@login_required(login_url="../../login")
def like_discussion(request,id):
    debate=Debate.objects.get(id=id)
    debate.like.add(request.user)
    debate.save()
    url="../../"+debate.slug+"!"
    return redirect(url)

@login_required(login_url="../../login")
def proslike(request,id):
    pros=Pros.objects.get(id=id)
    pros.proslike.add(request.user)
    pros.save()
    url="../../"+pros.debate_pros.slug+"!"
    return redirect(url)

@login_required(login_url="../../login")
def conslike(request,id):
    cons=Cons.objects.get(id=id)
    cons.conslike.add(request.user)
    cons.save()
    url="../../"+cons.debate_cons.slug+"!"
    return redirect(url)


def search(request):
    query = request.GET.get('search').lower()
    allProds = []
    debatetemp = Debate.objects.all()


    analyzed = query.split(" ")

    for i in analyzed:
        prod = [item for item in debatetemp if searchMatch(i, item)]
        if len(prod) != 0:
                    allProds.append(prod)



    temp = []
    for product in allProds:
        for i in product:
            temp.append(i)


    allProds = temp
    params = {'debate': allProds, "msg": "", "query": query}

    if len(allProds) == 0:
        params = {'msg': "No result found, we are adding new products daily so make sure to check again later",
                  "query": query}

    return render(request, 'debate/search.html', params)
    # return render(request, 'costumer/product.html', params)