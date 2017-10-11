from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    latest_event_list = Events.objects.order_by('-event_date')[:5]
    output = ', '.join([q.event_name for q in latest_event_list])
    return HttpResponse(output)

def detail(request, event_id):
    return HttpResponse("You're looking at event %s." % event_id)

def results(request, event_id):
    response = "You're looking at the results of event %s."
    return HttpResponse(response % question_id)

def select(request, question_id):
    return HttpResponse("You're selecting on timeslots %s." % question_id)
