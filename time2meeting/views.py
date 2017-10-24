from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Users, Events, TimeSlots


# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, 'time2meeting/index.html', context=None)


def guidance(request):
    return render(request, 'time2meeting/guidance.html', context=None)


def team(request):
    return render(request, 'time2meeting/team.html', context=None)

# def detail(request, event_id):
#     return HttpResponse("You're looking at event %s." % event_id)
#
# def results(request, event_id):
#     response = "You're looking at the results of event %s."
#     return HttpResponse(response % question_id)
#
# def select(request, question_id):
#     return HttpResponse("You're selecting on timeslots %s." % question_id)


def create_event(request):
    # need add exception
    if request.method == 'GET':
        return render(request, 'time2meeting/create_event.html', context=None)
    elif request.method == 'POST':
        event_name = request.POST.get('event_name')
        event = Events()
        event.event_name = event_name
        event.save()
        return HttpResponseRedirect(reverse('time2meeting:create_publish'))


def create_publish(request):
    if request.method == 'GET':
        return render(request, 'time2meeting/create_publish.html', context=None)


def delete_event(request, event_name, user_name):

    return HttpResponse("You're deleting.")


def select_timeslots(request):

    # return HttpResponseRedirect(reverse('time2meeting:results', args=(Events.event_id,)))
    return render(request, 'time2meeting/select_timeslots.html', context=None)


def get_result(request, event_name):
    # get timeslots and compute
    return True


def make_decision(request, event_name, user_name):
    result = get_result(request, event_name)
    if request == 'abort':
        return False
    elif request == 'decide':
        # update final decision
        return True

