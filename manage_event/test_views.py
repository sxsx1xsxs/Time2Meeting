from django.test import TestCase
from .models import Events, TimeSlots, EventUser
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.test import Client
from .views import *

class viewTestCase(TestCase):

    def setUp(self):
        thirty_mins = datetime.timedelta(minutes=30)
        time_now = timezone.now().replace(minute = 0,second=0, microsecond=0)

        # setup database
        self.organizer = User.objects.create(username = "organizer",
                                   email = "organizer@test.com")
        self.organizer.set_password('12345')
        self.organizer.save()
        self.participant1 = User.objects.create(username="participant1",
                                        email="participant1@test.com")
        self.participant2 = User.objects.create(username="participant2",
                                        email="participant2@test.com")
        self.event = Events.objects.create(event_name = "testEvent",
                                      time_range_start = time_now + thirty_mins*4,
                                      time_range_end = time_now + thirty_mins*6,
                                      deadline = time_now + thirty_mins*3,
                                      duration = thirty_mins)
        self.event_organizer = EventUser.objects.create(event=self.event,
                                             user=self.organizer,
                                             role='o')
        self.event_participant1 = EventUser.objects.create(event=self.event,
                                                  user=self.participant1,
                                                  role='p')
        self.event_participant2 = EventUser.objects.create(event=self.event,
                                                  user=self.participant2,
                                                  role='p')
        self.timeslot = TimeSlots.objects.create(event = self.event,
                                            user = self.organizer,
                                            time_slot_start = time_now + thirty_mins*4)
        self.timeslot1 = TimeSlots.objects.create(event=self.event,
                                                 user=self.participant1,
                                                 time_slot_start=time_now + thirty_mins * 4)
        self.timeslot2 = TimeSlots.objects.create(event=self.event,
                                                 user=self.participant2,
                                                 time_slot_start=time_now + thirty_mins * 6)

        # setup client
        self.client = Client()

    def test_get_result(self):
        result = get_result(self.event.id)
        self.assertEqual(result, {self.timeslot.time_slot_start:2, self.timeslot2.time_slot_start:1})

    def test_organize_index(self):
        login = self.client.login(username='organizer', password='12345')
        self.assertEqual(login, True)
        response = self.client.get(reverse('manage_event:organize_index', args=()))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['event_wait_for_decision'], [])
        self.assertQuerysetEqual(response.context['event_on_going'], ['<Events: testEvent>'])
        self.assertQuerysetEqual(response.context['event_history'], [])

