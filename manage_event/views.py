from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.utils import json
import sys
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile
from .forms import UserForm, ProfileForm


from .models import Users, Events, TimeSlots


# Create your views here.
from django.shortcuts import render


@login_required
def index(request):
    user_email = request.COOKIES.get('email')
    if not user_email:
        return render(request, 'manage_event/index.html')
    else:

        # return render(request, 'manage_event/index.html', context=None)
        # event_wait_for_decision = Events.objects.all()
        # latest_event_list = Events.objects.order_by('-event_date')[:5]
        # output = ', '.join([q.event_name for q in latest_event_list])
        return render(request, 'manage_event/index.html')

# def index(request):
#     get cookie by key
#     user_name = request.COOKIES.get('username')
#     if not user_name:
#         # set cookie:
#         # 1.initial a response;
#         # 2.set cookie(key, value);
#         # 3.return response to make the cookie change
#         response = HttpResponse('set cookie as wayne')
#         response.set_cookie('username', 'wayne')
#         return response
#     else:
#         response = HttpResponse('set cookie as null')
#         response.set_cookie('username', '')
#         return response


@login_required
def organize_index(request):

    print (request.user.email)
    event_wait_for_decision = Events.objects.filter(final_time_start__isnull = True).filter(deadline__lte= timezone.now())
    event_on_going = Events.objects.filter(deadline__gte= timezone.now())
    event_history = Events.objects.filter(final_time_start__isnull = False)
    #latest_event_list = Events.objects.order_by('-event_date')[:5]
    #output = ', '.join([q.event_name for q in latest_event_list])
    return render(request, 'manage_event/organize_index.html', {
        'event_wait_for_decision': event_wait_for_decision,
        'event_on_going': event_on_going,
        'event_history': event_history,
    })


@login_required
def participate_index(request):
    event_to_do = Events.objects.filter(deadline__gte= timezone.now())
    event_result = Events.objects.filter(final_time_start__isnull = False)
    event_pending = Events.objects.all()
    #latest_event_list = Events.objects.order_by('-event_date')[:5]
    #output = ', '.join([q.event_name for q in latest_event_list])
    return render(request, 'manage_event/participate_index.html', {
        'event_to_do' : event_to_do,
        'event_result': event_result,
        'event_pending': event_pending,

    })


# def detail(request, event_id):
#     return HttpResponse("You're looking at event %s." % event_id)
#
# def results(request, event_id):
#     response = "You're looking at the results of event %s."
#     return HttpResponse(response % question_id)
#
# def select(request, question_id):
#     return HttpResponse("You're selecting on timeslots %s." % question_id)


@login_required
def create_event(request):
    # need add exception
    if request.method == 'GET':
        return render(request, 'manage_event/create_event.html', context=None)
    elif request.method == 'POST':
        event_name = request.POST.get('event_name')
        time_range_start = request.POST.get('time_range_start')
        time_range_end = request.POST.get('time_range_end')
        duration = request.POST.get('duration')
        deadline = request.POST.get('deadline')

        if time_range_start is '' or time_range_end is '' or deadline is '' or event_name is '':
            return render(request, 'manage_event/create_event.html', context=None)
        else:
            event = Events()
            event.event_name = event_name
            event.time_range_start = time_range_start
            event.time_range_end = time_range_end
            event.duration = duration
            event.deadline = deadline
            event.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('manage_event:create_publish', args=(event.id,)))


@login_required
def create_publish(request, event_id):
    if request.method == 'GET':
        return render(request, 'manage_event/create_publish.html', {'event_id': event_id})


@login_required
def delete_event(request, event_name, user_name):


    return HttpResponseRedirect("You're deleting.")


@login_required
def select_timeslots(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    # return HttpResponseRedirect(reverse('time2meeting:results', args=(Events.event_id,)))
    return render(request, 'manage_event/select_timeslots.html', {'event': event})


@login_required
def get_result(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    # get timeslots and compute
    return []


@login_required
def make_decision_detail(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'manage_event/make_decision.html', {'event': event})


@login_required
def make_decision_results(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'manage_event/make_decision_results.html', {'event': event})


@login_required
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
        decision = event.decision_set.create(timeslot=selected_timeslot.timeslot)
        decision.save()
        event.final_decision = True
        event.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('manage_event:make_decision_results', args=(event.id,)))


@login_required
def show_decision_result(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'manage_event/show_decision_result.html', {'event': event})


@login_required
def get_each_user_timeslots(request, user_email, event_id):
    user_data = {}
    q1 = TimeSlots.objects.filter(event_id__gte = event_id)
    user_timeslots = q1.objects.filter(user_email__gte = user_email)
    for each in user_timeslots:
        date = each.date()
        time = each.time()
        user_data.setdefault([date,time], value = 1)
    return HttpResponse(simplejson.dumps(user_data), content_type='application/json')

@login_required
def all_user_timeslots(request, useruser_email, event_id):
    all_user_data = {}
    all_user_timeslots = TimeSlots.objects.filter(event_id__gte = event_id)
    for each in all_user_timeslots:
        date = each.date()
        time = each.time()
        l = [date, time]
        if l not in all_user_data:
            all_user_data.setdefault([date, time], value = 0)
        else:
            all_user_data[date, time] += 1
    return HttpResponse(simplejson.dumps(all_user_timeslots), content_type='application/json')

# def read_select_timeslots(request, user_email, event_id):
#     f = open('user_timeslots.json')
#     json_string = f.read()
#     data = json.loads(json_string)
#     f.close()


@login_required
def Home(request):
    return render(request, 'manage_event/index.html')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/manage_event/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'manage_event/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def webLogout(request):
    logout(request)
    return HttpResponseRedirect('/manage_event/')

