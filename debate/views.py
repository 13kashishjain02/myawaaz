from django.shortcuts import render
from debate.models import Debate
from django.http import HttpResponseRedirect, HttpResponse


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