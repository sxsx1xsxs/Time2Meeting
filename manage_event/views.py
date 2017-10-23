from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Users, Events, TimeSlots

# Create your views here.
def index(request):
    latest_event_list = Events.objects.order_by('-event_date')[:5]
    output = ', '.join([q.event_name for q in latest_event_list])
    return HttpResponse(output)

# def detail(request, event_id):
#     return HttpResponse("You're looking at event %s." % event_id)
#
# def results(request, event_id):
#     response = "You're looking at the results of event %s."
#     return HttpResponse(response % question_id)
#
# def select(request, question_id):
#     return HttpResponse("You're selecting on timeslots %s." % question_id)

def create_event(request, event_name, user_name):
    event = Events()
    event.event_name = event_name
    event.event_organizer = user_name

    return HttpResponse("You're creating.")

def delete_event(request, event_name, user_name):

    return HttpResponse("You're deleting.")

def select_timeslots(request, event_name, user_name, timeslot):

    return HttpResponseRedirect(reverse('manage_event:results', args=(Events.event_id,)))

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

