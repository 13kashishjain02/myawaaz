from django.shortcuts import render
from .models import Subject,Course
from .serializers import SubjectSerializer, CourseSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


@csrf_exempt
@api_view(['POST','GET','PUT','DELETE'])

def Subject_api(request,id=None):
    if request.method=="GET":
        if id is None:
            data=Subject.objects.all()
            serializer=SubjectSerializer(data,many=True)
            return Response(serializer.data)

        else:
            data=Subject.objects.filter(pk=id)
            serializer=SubjectSerializer(data,many=True)
            return Response(serializer.data)


    if request.method=='POST':
        serializer=SubjectSerializer(data=request.data)
       # print(serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg','DATA CREATED'})
        return Response(serializer.errors)

    if request.method=='PUT':
        data=Subject.objects.get(pk=id)
        serializer=SubjectSerializer(data,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg','Data Updated'})
        return Response(serializer.errors)

    if request.method=='DELETE':
        data=Subject.objects.get(pk=id)
        data.delete()
        return Response({'msg':'data deleted'})


