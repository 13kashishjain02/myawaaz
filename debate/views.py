from django.shortcuts import render
from debate.models import Debate
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import DebateSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

def post(request):
    debate=Debate.objects.create(title='title2',
                          pros={'pros': [], 'comment': [],},
                          cons={'cons': [], 'comment': [],}
                          )
    debate.save()
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




@csrf_exempt
@api_view(['POST','GET','PUT','DELETE'])
def comment_api(request,id=None):
    if request.method=="GET":
        if id is None:
            data=Debate.objects.all()
            serializer=DebateSerializer(data,many=True)
            print("hello",serializer.data)
            return Response(serializer.data)

        else:
            data=Debate.objects.filter(pk=id)
            serializer=DebateSerializer(data,many=True)
            print("hello",type(serializer.data))
            print("hello",serializer.data)
            return Response(serializer.data)


    if request.method=='POST':
        serializer=DebateSerializer(data=request.data)
        print(serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg','DATA CREATED'})
        return Response(serializer.errors)

    if request.method=='PUT':
        data=Debate.objects.get(pk=id)
        serializer=DebateSerializer(data,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            print("PUT data", serializer.data)
            return Response({'msg','Data Updated'})
        return Response(serializer.errors)

    if request.method=='DELETE':
        data=Debate.objects.get(pk=id)
        data.delete()
        return Response({'msg':'data deleted'})
