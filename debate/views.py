from django.shortcuts import render, redirect
from debate.models import Debate,Pros,Cons
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import DebateSerializer,ProsCommentSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    debate=Debate.objects.values()
    return render(request,"debate/index.html",{"debate":debate})

def post_view(request,slug):
    debate = Debate.objects.get(slug=slug)
    pros=Pros.objects.filter(debate_pros=debate)
    cons = Cons.objects.filter(debate_cons=debate)
    # return HttpResponse(slug)
    debate.tags=debate.tags.split(",")
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
    try:
        title='everyone should be vegan'
        slug = title.replace(" ", "-")
        debate=Debate.objects.create(title=title,slug=slug)
        debate.save()
    except IntegrityError as e:
        msg = "discussion with this title already exist"
        return HttpResponse(msg)
    return HttpResponse("done")

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

def comment(request,id):
    # Debate.objects.filter(data__owner__other_pets__0__name='Fishy')
    debate = Debate.objects.get(id=id)

    # section takes the value pros & cons depending on where the user posted his views
    section = "cons"

    # his view; what he commented is saved by comment
    comment = "point 4"

    # name=request.user.name
    name='ram'

    if section == "pros":
        debate.pros['comment'].append({'name': name, 'comment':comment})
        debate.save()
    else:
        debate.cons['comment'].append({'name': name, 'comment':comment})
        debate.save()
    return HttpResponse("done")


def add_pros(request,id):
    debate=Debate.objects.get(id=id)
    pros = Pros.objects.create(debate_pros=debate,pros="pros2")
    pros.save()
    return HttpResponse("done")

def add_cons(request,id):
    debate=Debate.objects.get(id=id)
    cons = Cons.objects.create(debate_cons=debate,cons="cons2")
    cons.save()
    return HttpResponse("done")

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