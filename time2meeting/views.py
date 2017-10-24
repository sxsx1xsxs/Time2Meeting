from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Users, Events, TimeSlots, Results, Decision


# Create your views here.
from django.shortcuts import render


def index(request):

    event_wait_for_decision = Events.objects.all()
    #latest_event_list = Events.objects.order_by('-event_date')[:5]
    #output = ', '.join([q.event_name for q in latest_event_list])
    return render(request, 'manage_event/organize_index.html', {
        'event_wait_for_decision' : event_wait_for_decision,
    })

def organize_index(request):
    event_wait_for_decision = Events.objects.all()
    event_on_going = Events.objects.all()
    #latest_event_list = Events.objects.order_by('-event_date')[:5]
    #output = ', '.join([q.event_name for q in latest_event_list])
    return render(request, 'manage_event/organize_index.html', {
        'event_wait_for_decision' : event_wait_for_decision,
        'event_on_going' : event_on_going,
    })

def participate_index(request):
    event_to_do = Events.objects.all()
    event_result = Events.objects.all()
    event_pending = Events.objects.all()
    #latest_event_list = Events.objects.order_by('-event_date')[:5]
    #output = ', '.join([q.event_name for q in latest_event_list])
    return render(request, 'manage_event/participate_index.html', {
        'event_to_do' : event_to_do,
        'event_result': event_result,
        'event_pending': event_pending,

    })

    #return render(request, 'time2meeting/index.html', context=None)


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


def get_result(request):
    # get timeslots and compute
    return True

# def make_decision_index(request):
#
#     #selected_choice = TimeSlots.get(pk=request.POST['choice'])
#     timeslots = TimeSlots.objects
#     return render(request, 'manage_event/make_decision.html', context={
#         'timeslots':timeslots,
#     })
#
# def make_decision(request):
#
#     return HttpResponse("You have make decision.")

    # result = get_result(request)
    # if request == 'abort':
    #     return False
    # elif request == 'decide':
    #     # update final decision
    #     return True

def make_decision_detail(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'manage_event/make_decision.html', {'event': event})

def make_decision_results(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'manage_event/make_decision_results.html', {'event': event})

def make_decision(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    try:
        selected_timeslot = event.timeslots_set.get(pk=request.POST['time_slot'])
    except (KeyError, TimeSlots.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'manage_event/make_decision.html', {
            'event': event,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_timeslot.is_decision += 1
        selected_timeslot.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('manage_event:make_decision_results', args=(event.id,)))