from django.test import TestCase
from django.contrib.auth.models import User
from .forms import EventForm
from .models import Events
from django.core.exceptions import ValidationError

# Create your tests here.

user_data = {
    'email': 'shadow.lzd@gmail.com',
    'username': 'shadow.lzd'
}

event_data = {
    'event_name': 'shadow',
    'time_range_start': '2017-10-01',
    'time_range_end': '2017-10-08',
    'deadline': '2017-10-01',
    'duration': '30'
}

timeslots_data = {
    'event': 'shadow',
    'user': '2017-10-01',
    'time_range_end': '2017-10-08',
    'deadline': '2017-10-01',
    'duration': '30'
}


def create_user(**kwargs):
    return User.objects.create_user(**kwargs)


# def create_event(user, **kwargs):
#     event = Events.objects.create(**kwargs)
#     eventuser = EventUser.objects.create(user=user, event=event, role='o')
#     return {
#             'event': event,
#             'eventuser': eventuser
#     }
#
#
# def select_timeslots(**kwargs):
#     timeslots = timeslots.objects.create()
#     return


class EventsTestCase(TestCase):

    def test_time_range_start(self):
        # event = Events.objects.filter(event_name=481).update(time_range_start='')
        # assertRaises(ValidationError)
        return

#     def test_time_range_end(self):
#         event = Events.objects.filter(event_name=481).update(time_range_start='')
#         assertRaises(ValidationError)
#
#     def test_dealine(self):
#         event = Events.objects.filter(event_name=481).update(time_range_start='')
#         assertRaises(ValidationError)
#
#
# class TimeSlotsTestCase(TestCase):
#     def test_time_slots_start(self):
#         timeslots = TimeSlots.objects.filter(event=1).update(timeslots_start='')
#         assertRaises(ValidationError)
