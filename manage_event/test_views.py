from django.test import TestCase
from .models import Events, TimeSlots, EventUser
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.test import Client
from .views import *


class viewTestCase(TestCase):

    def setUp(self):
        """
        setup all the objects needed for the tests

        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_now = datetime.datetime.now().replace(minute = 0,second=0, microsecond=0)

        # setup database
        self.organizer = User.objects.create(username = "organizer",
                                             email = "organizer@test.com")
        self.organizer.set_password('12345')
        self.organizer.save()
        self.participant1 = User.objects.create(username="participant1",
                                                email="participant1@test.com")
        self.participant2 = User.objects.create(username="participant2",
                                                email="participant2@test.com")
        # Question: time_range_end represents the start or end of the half hour, currently regards as the end.
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
                                                 time_slot_start = time_now + thirty_mins * 4)
        self.timeslot1 = TimeSlots.objects.create(event=self.event,
                                                  user=self.participant1,
                                                  time_slot_start=time_now + thirty_mins * 4)
        self.timeslot2 = TimeSlots.objects.create(event=self.event,
                                                  user=self.participant2,
                                                  time_slot_start=time_now + thirty_mins * 5)
        # setup client and login
        self.client = Client()
        login = self.client.login(username='organizer', password='12345')
        self.assertEqual(login, True)

    def test_get_result(self):
        """
        Since get_result() is an internal function, just test the return value of it.

        """
        result = get_result(self.event.id)
        self.assertEqual(result, {self.timeslot.time_slot_start:2, self.timeslot2.time_slot_start:1})

    def test_organize_index(self):
        """
        Test the response of a GET request when calling organize_index.

        """
        response = self.client.get(reverse('manage_event:organize_index', args=()))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['event_wait_for_decision'], [])
        self.assertQuerysetEqual(response.context['event_on_going'], ['<Events: testEvent>'])
        self.assertQuerysetEqual(response.context['event_history'], [])

    def test_participate_index(self):
        """
        Test the response of a GET request when calling participate_index.

        """
        response = self.client.get(reverse('manage_event:participate_index', args=()))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['event_to_do'], [])
        self.assertQuerysetEqual(response.context['event_done'], ['<Events: testEvent>'])
        self.assertQuerysetEqual(response.context['event_result'], [])
        self.assertQuerysetEqual(response.context['event_pending'], [])

    def test_pending(self):
        """
        Test the response of a GET request when calling pending.

        """
        response = self.client.get(reverse('manage_event:pending', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)
        self.assertListEqual(response.context['timeslots'], [self.timeslot.time_slot_start.strftime('%Y-%m-%d %H:%M:%S')])

    def test_on_going(self):
        """
        Test the response of a GET request when calling on_going.

        """
        response = self.client.get(reverse('manage_event:on_going', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)

    def test_make_decision_detail(self):
        """
        Test the response of a GET request when calling make_decision_detail.

        """
        response = self.client.get(reverse('manage_event:make_decision_detail', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)

    def test_make_decision_results(self):
        """
        Test the response of a GET request when calling make_decision_results.

        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        event = Events.objects.create(event_name="testEvent",
                                      time_range_start=time_now + thirty_mins * 4,
                                      time_range_end=time_now + thirty_mins * 6,
                                      final_time_start=time_now + thirty_mins * 5,
                                      final_time_end=time_now + thirty_mins * 6,
                                      deadline=time_now + thirty_mins * 3,
                                      duration=thirty_mins)
        response = self.client.get(reverse('manage_event:make_decision_results', args=(event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], event)

    def test_make_decision_json(self):
        """
        Test the json of a GET request when calling make_decision_json.

        """
        response = self.client.get(reverse('manage_event:make_decision_json', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {self.timeslot.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'):'2',
                              self.timeslot2.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'):'1'})

    def test_make_decision_post(self):
        """
        Test the modification of DB of a POST request when calling make_decision.

        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        event = Events.objects.create(event_name="testEvent",
                                      time_range_start=time_now + thirty_mins * 4,
                                      time_range_end=time_now + thirty_mins * 6,
                                      deadline=time_now + thirty_mins * 3,
                                      duration=thirty_mins)
        decision = {self.timeslot.time_slot_start.strftime('%Y-%m-%d %H:%M:%S') : "Blank",
                    self.timeslot2.time_slot_start.strftime('%Y-%m-%d %H:%M:%S') : "Selected"}
        response = self.client.post(reverse('manage_event:make_decision', args=(event.id,)),
                                    json.dumps(decision),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # At this point, event in DB has updated, but the object here is not updated, it needs to be reloaded from DB
        event.refresh_from_db()
        self.assertEqual(event.final_time_start, self.timeslot2.time_slot_start)
        self.assertEqual(event.final_time_end, self.timeslot2.time_slot_start + datetime.timedelta(minutes=30))

    def test_make_decision_get(self):
        """
        Test the response of a GET request when calling make_decision.

        """
        response = self.client.get(reverse('manage_event:make_decision_render', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)

    def test_make_decision_render_error(self):
        """
        Test the response of a GET request when calling make_decision_render with error.

        """
        response = self.client.get(reverse('manage_event:make_decision_render', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)
        self.assertEqual(response.context['error_message'], "You didn't make a decision.")

    def test_make_decision_render(self):
        """
        Test the response of a GET request when calling make_decision_render.

        """
        self.event.final_time_start = self.timeslot.time_slot_start.strftime('%Y-%m-%d %H:%M:%S')
        self.event.save()
        final_time_end = self.timeslot.time_slot_start + datetime.timedelta(minutes=30)
        self.event.final_time_end = final_time_end.strftime('%Y-%m-%d %H:%M:%S')
        self.event.save()
        response = self.client.get(reverse('manage_event:make_decision_render', args=(self.event.id,)))
        self.assertRedirects(response, reverse('manage_event:make_decision_results', args=(self.event.id,)))

    def test_show_decision_result(self):
        """
        Test the response of a GET request when calling show_decision_result.

        """
        response = self.client.get(reverse('manage_event:show_decision_result', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)

    def test_create_event_get(self):
        """
        Test the GET response of view create event
        :return:
        """
        response = self.client.get(reverse('manage_event:create_event'))
        self.assertEqual(response.status_code, 200)

    def test_create_event_post(self):
        """
        Test the POST response of view create event
        :return:
        """

        thirty_mins = datetime.timedelta(minutes=30)
        time_now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        event = Events.objects.create(event_name="testEvent",
                                      time_range_start=time_now + thirty_mins * 4,
                                      time_range_end=time_now + thirty_mins * 6,
                                      deadline=time_now + thirty_mins * 3,
                                      duration=thirty_mins)
        decision = {self.timeslot.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'): "Blank",
                    self.timeslot2.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'): "Selected"}
        response = self.client.post(reverse('manage_event:make_decision', args=(event.id,)),
                                    json.dumps(decision),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # At this point, event in DB has updated, but the object here is not updated, it needs to be reloaded from DB
        event.refresh_from_db()
        self.assertEqual(event.final_time_start, self.timeslot2.time_slot_start)
        self.assertEqual(event.final_time_end, self.timeslot2.time_slot_start + datetime.timedelta(minutes=30))
