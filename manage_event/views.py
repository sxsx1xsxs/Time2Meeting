from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import datetime, json
import sys
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db import transaction
from .models import Profile

from .forms import UserForm, ProfileForm, EventForm, InvitationForm, AbortForm
from .models import Events, TimeSlots, EventUser, AbortMessage
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


@login_required
def index(request):
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

    #print(request.user.email)
    organized_events = EventUser.objects.filter(user=request.user).filter(role="o")
    organized_events_id = []

    for organized_event in organized_events:
        organized_events_id.append(organized_event.event.id)

    event_wait_for_decision = Events.objects.filter(id__in=organized_events_id).filter(final_time_start__isnull=True).filter(deadline__lte=datetime.datetime.now())
    event_on_going = Events.objects.filter(id__in=organized_events_id).filter(deadline__gte=datetime.datetime.now())
    event_history = Events.objects.filter(id__in=organized_events_id).filter(final_time_start__isnull=False)
    #latest_event_list = Events.objects.order_by('-event_date')[:5]
    #output = ', '.join([q.event_name for q in latest_event_list])
    return render(request, 'manage_event/organize_index.html', {
        'event_wait_for_decision': event_wait_for_decision,
        'event_on_going': event_on_going,
        'event_history': event_history,
    })


@login_required
def participate_index(request):

    participate_events = EventUser.objects.filter(user=request.user)
    participate_events_id = []
    for participate_event in participate_events:
        participate_events_id.append(participate_event.event.id)

    to_do_events_id = []
    done_events_id = []
    for participate_event_id in participate_events_id:
        if TimeSlots.objects.filter(user=request.user).filter(event_id = participate_event_id).count() == 0:
            #print(TimeSlots.objects.filter(user=request.user).filter(event_id = participate_event_id))
            to_do_events_id.append(participate_event_id)
        else:
            done_events_id.append(participate_event_id)

    event_to_do = Events.objects.filter(id__in = to_do_events_id).filter(deadline__gte= datetime.datetime.now())
    event_done = Events.objects.filter(id__in = done_events_id).filter(deadline__gte=datetime.datetime.now())
    event_result = Events.objects.filter(id__in = participate_events_id).filter(final_time_start__isnull = False)
    event_pending = Events.objects.filter(id__in = participate_events_id).filter(deadline__lte=datetime.datetime.now()).exclude(final_time_start__isnull = False)
    #latest_event_list = Events.objects.order_by('-event_date')[:5]
    #output = ', '.join([q.event_name for q in latest_event_list])
    return render(request, 'manage_event/participate_index.html', {
        'event_to_do' : event_to_do,
        'event_done' : event_done,
        'event_result': event_result,
        'event_pending': event_pending,

    })

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_data = form.cleaned_data
            event = Events.objects.create(**event_data)
            event.save()

            # create corresponding EventUser tuple.
            eventuser_data = {'event': event,
                              'user': request.user,
                              'role': 'o'
                              }
            eventuser = EventUser.objects.create(**eventuser_data)
            eventuser.save()
            return HttpResponseRedirect(reverse('manage_event:create_publish', args=(event.pk,)))
    else:
        form = EventForm(initial={'info': 'description of this event.'})
    return render(request, 'manage_event/create_event.html', {'form': form})


@login_required
def create_publish(request, event_id):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            emails = form.cleaned_data
            for email in emails:
                user_name = email.rsplit('@', 1)[0]
                user = User.objects.get_or_create(username=user_name, email=email)[0]
                event = Events.objects.get(pk=event_id)
                EventUser.objects.get_or_create(user=user, event=event)

                messages.success(request, _('Invite Success!'))
            return HttpResponseRedirect(reverse('manage_event:create_publish', args=(event_id,)))
    else:
        form = InvitationForm()
    return render(request, 'manage_event/create_publish.html', {'event_id': event_id, 'form': form})

@login_required
def abort_event_detail(request, event_id):
    event = get_object_or_404(Events, pk=event_id)

    if EventUser.objects.get(event = event, user= request.user).role == 'o':
        if request.method == 'POST':
            form = AbortForm(request.POST)
            if form.is_valid():
                AbortMessage.objects.get_or_create(event=event, Abortion_message=form.cleaned_data['Abortion_message'])
                event.status = 'Abort'
                event.save()
            return HttpResponseRedirect(reverse('manage_event:abort_event_result', args=(event_id,)))
        else:
            form = AbortForm()
            contents = {'event': event,
                        'message': "Cautious: Once the event is aborted, it cannot be undo. Every participants will be infomed with the abortion message.)",
                        'form': form.as_p()}
    else:
        contents = {'event': event,
                    'error_message': "Sorry, you didn't have the access to abort this event."}
    return render(request, 'manage_event/abort_event_detail.html', contents)

@login_required
def abort_event_result(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'manage_event/abort_event_result.html', {'event': event})

@login_required
def delete_event(request, event_id):

    return HttpResponseRedirect("You're deleting.")

@login_required
def pending(request, event_id):
    event = get_object_or_404(Events, pk=event_id)

    timeslots = TimeSlots.objects.filter(event= event).filter(user=request.user)
    show_timeslots = []
    for t in timeslots:
        show_timeslots.append(t.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'))

    context = {'event': event, 'timeslots': show_timeslots}
    return render(request, 'manage_event/pending.html', context)

@login_required
def on_going(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    # on_going.html will call make_decision_json for data
    return render(request, 'manage_event/on_going.html', {'event': event})

def get_result(event_id):
    """
    Get result based on all the time slots users provided.
    :param event_id:
    :return: A dictionary of the (time slot, number of available person) pair.
    """
    event = get_object_or_404(Events, pk=event_id)
    timeslots = event.timeslots_set.all()

    result = {}
    for timeslot in timeslots:
        time_slot_start = timeslot.time_slot_start
        if not result.get(time_slot_start):
            result[time_slot_start] = 1
        else:
            result[time_slot_start] += 1

    return result

@login_required
def make_decision_detail(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    # make_decision.html will call make_decision_json for data
    return render(request, 'manage_event/make_decision.html', {'event': event})


@login_required
def make_decision_results(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'manage_event/make_decision_results.html', {'event': event})


def make_decision_json(request, event_id):
    """
    Used for .js parsing json by ajax.
    :param request:
    :param event_id:
    :return:
    """
    event = get_object_or_404(Events, pk=event_id)
    result = get_result(event_id)
    # result = {datetime.datetime(2017, 10, 20, 23, 30):1}
    time_range_start = event.time_range_start
    time_range_end = event.time_range_end

    # Make json data according to contract
    result_data = {}
    time = time_range_start
    thirty_mins = datetime.timedelta(minutes=30)
    while time < time_range_end:
        if not result.get(time):
            result_data[time.strftime("%Y-%m-%d %H:%M:%S")] = '0'
        else:
            result_data[time.strftime("%Y-%m-%d %H:%M:%S")] = str(result[time])
        time += thirty_mins
    result_json = json.dumps(result_data)

    return HttpResponse(result_json, content_type='application/json')


@login_required
def make_decision(request, event_id):
    event = get_object_or_404(Events, pk=event_id)

    if request.method == 'POST':
        decision_json = json.loads(request.body.decode("utf-8"))
        for key in decision_json:
            if decision_json[key] == "Selected":
                event.final_time_start = datetime.datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
                event.save()
                for key_1 in decision_json:
                    if decision_json[key_1] == "Selected":
                        event.final_time_end = datetime.datetime.strptime(key_1, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=30)
                        event.save()

                name = request.POST.get('name')
                dict = {'name': name}
                return HttpResponse(json.dumps(dict), content_type='application/json')

    name = request.POST.get('name')
    dict = {'name': name}

    return HttpResponse(json.dumps(dict), content_type='application/json')


@login_required
def make_decision_render(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    if event.final_time_start and event.final_time_end:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('manage_event:make_decision_results', args=(event.id,)))
    else:
        return render(request, 'manage_event/make_decision.html', {
            'event': event,
            'error_message': "You didn't make a decision.",
        })

@login_required
def show_decision_result(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'manage_event/show_decision_result.html', {'event': event})

#
# @login_required
# def get_each_user_timeslots(request, user, event_id):
#     event = get_object_or_404(Events, pk=event_id)
#     time_range_start = event.time_range_start
#     time_range_end = event.time_range_end
#     q1 = TimeSlots.objects.filter(event_id__gte = event_id)
#     user_timeslots = q1.objects.filter(user_email__gte = user_email)
#
#     # Make json data according to contract
#     user_data = {}
#     time = time_range_start
#     thirty_mins = datetime.timedelta(minutes=30)
#
#     while time < time_range_end:
#         if not user_timeslots.get(time):
#             user_data[time.strftime("%Y-%m-%d %H:%M:%S")] = "Blank"
#         else:
#             user_data[time.strftime("%Y-%m-%d %H:%M:%S")] = "Selected"
#         time = thirty_mins
#     dumps = json.dumps(user_data)
#     return HttpResponse(dumps, content_type='application/json')


#
#
# @login_required
# def all_user_timeslots(request, useruser_email, event_id):
#
#     event = get_object_or_404(Events, pk=event_id)
#
#     time_range_start = event.time_range_start
#     time_range_end = event.time_range_end
#     result = get_result(event_id)
#
#     all_user_data = {}
#     all_user_timeslots = TimeSlots.objects.filter(event_id__gte = event_id)
#
#     while time < time_range_end:
#         if not all_user_timeslots.get(time):
#             user_data[time.strftime("%Y-%m-%d %H:%M:%S")] = "Blank"
#         else:
#             user_data[time.strftime("%Y-%m-%d %H:%M:%S")] = result[time]
#         time = thirty_mins
#     dumps = json.dumps(user_data)
#     return HttpResponse(simplejson.dumps(all_user_timeslots), content_type='application/json')


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


@login_required
def select_timeslots(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    # used for join event through link
    if EventUser.objects.filter(user = request.user).filter(event = event).count() == 0:
        event_user, create= EventUser.objects.update_or_create(event = event, user = request.user, role = "p")
    #return HttpResponseRedirect(reverse('manage_event:select_publish', args=(event.id,)))
    return render(request, 'manage_event/select_timeslots.html', {'event': event})


@login_required
def modify_timeslots(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    #return HttpResponseRedirect(reverse('manage_event:select_publish', args=(event.id,)))
    return render(request, 'manage_event/modify_timeslots.html', {'event': event})


@login_required
def read_timeslots(request, event_id):
    print('read time slots')
    event = get_object_or_404(Events, pk=event_id)
    # user = request.user.email
    # user = Users.objects.create(pk = "qimenghan77@gmail.com", user_name = "qimeng")
    # user.save()
    print(request.user.email)
    user = request.user
    """
    Read the Json file includes user selection information and update the database
    """
    # f = open('user_timeslots.json')
    # json_string = f.read()
    #json.loads retruns a list that contains a dictionary
    # data = json.loads(json_string)
    # f.close()

    s = """{
  	"2017-10-10 18:30:00": "Selected",
  	"2017-10-10 19:00:00": "Blank",
  	"2017-10-11 18:30:00": "Selected",
  	"2017-10-11 19:00:00": "Blank",
  	"2017-10-12 18:30:00": "Selected",
  	"2017-10-12 19:00:00": "Blank",
  	"2017-10-13 18:30:00": "Selected",
  	"2017-10-13 19:00:00": "Blank",
  	"2017-10-14 18:30:00": "Selected",
  	"2017-10-14 19:00:00": "Blank",
  	"2017-10-15 18:30:00": "Selected",
  	"2017-10-15 19:00:00": "Blank"
      }"""
    if request.method == 'POST':
        json_data = json.loads(request.body)
    if request.method == 'GET':
        json_data = json.loads(s)
    dict_data = json_data
    print(TimeSlots.objects.all())
    for key, value in dict_data.items():
        if (value == "Selected"):
            user_time_slot = TimeSlots.objects.update_or_create(event= event,
            user = user, time_slot_start = key)
    # return redirect("")
    return HttpResponseRedirect(reverse('manage_event:select_publish', args=(event.id,)))

@login_required
def initialize_timeslots(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    time_range_start = event.time_range_start
    time_range_end = event.time_range_end
    # Make json data according to contract
    user_data = {}
    time = time_range_start
    thirty_mins = datetime.timedelta(minutes=30)

    while time < time_range_end:
        user_data[time.strftime("%Y-%m-%d %H:%M:%S")] = "Blank"
            #print(time.strftime("%Y-%m-%d %H:%M:%S"))
            #print(user_data[time.strftime("%Y-%m-%d %H:%M:%S")])
        time += thirty_mins
    dumps = json.dumps(user_data)
    return HttpResponse(dumps, content_type='application/json')



@login_required
def select_publish(request, event_id):
    name = request.POST.get('name')
    dict = {'name': name}
    return HttpResponse(json.dumps(dict), content_type='application/json')
    # return HttpResponse("OK")
    # return render(request, 'manage_event/select_timeslots.html', context)


def select_publish_render(request, event_id):
    event = get_object_or_404(Events, pk=event_id)

    #pass the event name to the html page
    timeslots = TimeSlots.objects.filter(event= event)
    show_timeslots = []
    for t in timeslots:
        show_timeslots.append(t.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'))
    # print(t.time_slot_start.strftime('%Y-%m-%d %H:%M'))
    # timeslots.extra(select={'time_slot_start':"DATE_FORMAT(activation_date, '%Y-%m-%d')"})
    # timeslots = (timeslots.values_list('time_slot_start', flat=True))
    # timeslots = list(timeslots.extra(select={'time_slot_start':"DATE_FORMAT(activation_date, '%Y-%m-%d')"}).values_list('date', flat='true')
    # timeslots = timeslots.values('datestr')
    # print(type(timeslots.all()))
    # print(timeslots.all())
    context = {'event': event, 'timeslots': show_timeslots}
    print("select publish render")
    print(context)
    return render(request, 'manage_event/select_publish.html', context)

@login_required
def modify_timeslots_read(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    time_range_start = event.time_range_start
    time_range_end = event.time_range_end
    q1 = TimeSlots.objects.filter(event=event)
    user_timeslots = q1.filter(user= request.user)
    # Make json data according to contract
    user_data = {}
    time = time_range_start
    thirty_mins = datetime.timedelta(minutes=30)

    while time < time_range_end:
        if not user_timeslots.filter(time_slot_start = time):
            user_data[time.strftime("%Y-%m-%d %H:%M:%S")] = "Blank"
            print(time.strftime("%Y-%m-%d %H:%M:%S"))
            print(user_data[time.strftime("%Y-%m-%d %H:%M:%S")])
        else:
            user_data[time.strftime("%Y-%m-%d %H:%M:%S")] = "Selected"
        time += thirty_mins
    dumps = json.dumps(user_data)
    return HttpResponse(dumps, content_type='application/json')


@login_required
def modify_timeslots_update(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    user = request.user
    q1 = TimeSlots.objects.filter(event=event)
    user_timeslots = q1.filter(user=user)
    user_timeslots.delete()

    if request.method == 'POST':
        json_data = json.loads(request.body)
        dict_data = json_data



    if request.method == 'GET':
        s = """{
      	"2017-10-10 18:30:00": "Blank",
      	"2017-10-10 19:00:00": "Blank",
      	"2017-10-11 18:30:00": "Blank",
      	"2017-10-11 19:00:00": "Blank",
      	"2017-10-12 18:30:00": "Selected",
      	"2017-10-12 19:00:00": "Selected",
      	"2017-10-13 18:30:00": "Selected",
      	"2017-10-13 19:00:00": "Blank",
      	"2017-10-14 18:30:00": "Selected",
      	"2017-10-14 19:00:00": "Blank",
      	"2017-10-15 18:30:00": "Selected",
      	"2017-10-15 19:00:00": "Blank"
          }"""
        dict_data = json.loads(s)
    #print(TimeSlots.objects.all())
    for key, value in dict_data.items():
        if (value == "Selected"):
            user_time_slot = TimeSlots.objects.update_or_create(event = event,
            user = user, time_slot_start = key)
    return HttpResponseRedirect(reverse('manage_event:select_publish', args=(event.id,)))
