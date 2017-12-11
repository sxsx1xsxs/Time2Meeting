import ast
# import datetime
from django.test import TestCase
from django.test import Client
from .views import *
# from .models import Events, TimeSlots, EventUser
# from django.contrib.auth.models import User
# from django.utils import timezone


class viewTestCase(TestCase):
    """
    Test cases for views.py.
    """

    def setUp(self):
        """
        setup all the objects needed for the tests

        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

        # setup database
        self.organizer = User.objects.create(username="organizer",
                                             email="organizer@test.com")
        self.organizer.set_password('12345')
        self.organizer.save()
        self.participant1 = User.objects.create(username="participant1",
                                                email="participant1@test.com")
        self.participant1.set_password('12345')
        self.participant1.save()
        self.participant2 = User.objects.create(username="participant2",
                                                email="participant2@test.com")
        # Question: time_range_end represents the start or end of the half hour, currently regards as the end.
        self.event = Events.objects.create(event_name="testEvent",
                                           time_range_start=time_now + thirty_mins*4,
                                           time_range_end=time_now + thirty_mins*6,
                                           deadline=time_now + thirty_mins*3,
                                           duration=thirty_mins)

        self.event_organizer = EventUser.objects.create(event=self.event,
                                                        user=self.organizer,
                                                        role='o')
        self.event_participant1 = EventUser.objects.create(event=self.event,
                                                           user=self.participant1,
                                                           role='p')
        self.event_participant2 = EventUser.objects.create(event=self.event,
                                                           user=self.participant2,
                                                           role='p')
        self.timeslot = TimeSlots.objects.create(event=self.event,
                                                 user=self.organizer,
                                                 time_slot_start=time_now + thirty_mins * 4)
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
        self.assertEqual(result, {self.timeslot.time_slot_start: 2, self.timeslot2.time_slot_start: 1})

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

    def test_make_decision_json(self):
        """
        Test the json of a GET request when calling make_decision_json.

        """
        response = self.client.get(reverse('manage_event:make_decision_json', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {self.timeslot.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'): '2',
                              self.timeslot2.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'): '1'})

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
        self.assertRedirects(response,
                             reverse('manage_event:make_decision_results', args=(self.event.id,)))

    def test_show_decision_result(self):
        """
        Test the response of a GET request when calling show_decision_result.

        """
        response = self.client.get(reverse('manage_event:show_decision_result', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)

    def test_select_publish_render(self):
        """
        Test the response of a GET request when calling select_publish_render.
        """
        response = self.client.get(reverse('manage_event:select_publish_render', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)
        show_timeslots = []
        show_timeslots.append(self.timeslot.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response.context['timeslots'], show_timeslots)

    def test_modify_timeslots(self):
        """
        Test the response of a GET request when calling modify_timeslots.
        """
        response = self.client.get(reverse('manage_event:modify_timeslots', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)

    def test_select_timeslots(self):
        """
        Test the response of a GET request when calling select_timeslots.
        """
        response = self.client.get(reverse('manage_event:select_timeslots', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event'], self.event)

    def test_initialize_timeslots(self):
        """
        Test the json of a GET request when calling initialize_timeslots.
        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.event1 = Events.objects.create(event_name="testEvent",
                                            time_range_start=time_now + thirty_mins*30,
                                            time_range_end=time_now + thirty_mins*144,
                                            deadline=time_now + thirty_mins*24,
                                            duration=thirty_mins*2)
        response = self.client.get(reverse('manage_event:initialize_timeslots', args=(self.event1.id,)))
        jsonstring = str(response.content, encoding='utf8')
        json = ast.literal_eval(jsonstring)
        for key, value in json.items():
            self.assertEqual(value, "Blank")

    def test_modify_event_deadline(self):
        """
        Test the post request for the test_modify_event_deadline
        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_range_start = datetime.datetime(2018, 2, 10, 2, 0, 0, 0)
        time_range_end = datetime.datetime(2018, 2, 15, 20, 0, 0, 0)
        deadline = datetime.datetime(2018, 1, 1, 0, 0, 0, 0)
        self.event1 = Events.objects.create(event_name="testEvent",
                                            time_range_start=time_range_start,
                                            time_range_end=time_range_end,
                                            deadline=deadline,
                                            duration=thirty_mins*2)
        self.event1.save()
        self.event_user = EventUser.objects.create(event = self.event1, user = self.organizer)
        self.event_user.save()
        user_input3 = datetime.datetime(2018, 2, 9, 0, 0, 0, 0)
        post_dict = {'deadline': user_input3}
        response1 = self.client.post(reverse('manage_event:modify_event_deadline_detail', args=(self.event1.id,)),post_dict)
        event = get_object_or_404(Events, pk=self.event1.id)
        self.assertEqual(event.deadline, user_input3)


    def test_read_timeslots(self):
        """
        Test the POST response of read timeslots from json file and change database.
        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_range_start = datetime.datetime(2018, 2, 10, 2, 0, 0, 0)
        time_range_end = datetime.datetime(2018, 2, 15, 20, 0, 0, 0)
        deadline = datetime.datetime(2018, 1, 1, 0, 0, 0, 0)
        self.event1 = Events.objects.create(event_name="testEvent",
                                            time_range_start=time_range_start,
                                            time_range_end=time_range_end,
                                            deadline=deadline,
                                            duration=thirty_mins*2)
        jsondict = {"2018-02-10 18:30:00": "Selected",
                    "2018-02-10 19:00:00": "Blank",
                    "2018-02-11 18:30:00": "Selected",
                    "2018-02-11 19:00:00": "Blank",
                    "2018-02-12 18:30:00": "Selected",
                    "2018-02-12 19:00:00": "Blank",
                    "2018-02-13 18:30:00": "Selected",
                    "2018-02-13 19:00:00": "Blank",
                    "2018-02-14 18:30:00": "Selected",
                    "2018-02-14 19:00:00": "Blank",
                    "2018-02-15 18:30:00": "Selected",
                    "2018-02-15 19:00:00": "Blank"}
        response = self.client.post(reverse('manage_event:read_timeslots', args=(self.event1.id,)),
                                    json.dumps(jsondict), content_type="application/json")
        event_timeslots = TimeSlots.objects.filter(event=self.event1, user=self.organizer)
        self.event1.refresh_from_db()
        q = TimeSlots.objects.filter(event=self.event1, user=self.organizer)
        d = []
        for Q in q:
            d.append(Q.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'))
        for key, value in jsondict.items():
            if value == "Selected":
                self.assertIn(key, d)
            if value == "Blank":
                self.assertNotIn(key, d)

    def test_modify_timeslots_read(self):
        """
        Test the json of a GET request when calling modify_timeslots_read.
        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_range_start = datetime.datetime(2018, 2, 10, 2, 0, 0, 0)
        time_range_end = datetime.datetime(2018, 2, 10, 6, 0, 0, 0)
        deadline = datetime.datetime(2018, 1, 1, 0, 0, 0, 0)
        self.event1 = Events.objects.create(event_name="testEvent",
                                            time_range_start=time_range_start,
                                            time_range_end=time_range_end,
                                            deadline=deadline,
                                            duration=thirty_mins*2)
        self.timeslot1 = TimeSlots.objects.create(event=self.event1,
                                                  user=self.organizer,
                                                  time_slot_start=datetime.datetime(2018, 2, 10, 2, 0, 0, 0))
        self.timeslot2 = TimeSlots.objects.create(event=self.event1,
                                                  user=self.organizer,
                                                  time_slot_start=datetime.datetime(2018, 2, 10, 2, 30, 0, 0))
        self.timeslot2 = TimeSlots.objects.create(event=self.event1,
                                                  user=self.organizer,
                                                  time_slot_start=datetime.datetime(2018, 2, 10, 3, 0, 0, 0))
        expected_json = {"2018-02-10 02:00:00": "Selected",
                         "2018-02-10 02:30:00": "Selected",
                         "2018-02-10 03:00:00": "Selected",
                         "2018-02-10 03:30:00": "Blank",
                         "2018-02-10 04:00:00": "Blank",
                         "2018-02-10 04:30:00": "Blank",
                         "2018-02-10 05:00:00": "Blank",
                         "2018-02-10 05:30:00": "Blank"}
        response = self.client.get(reverse('manage_event:modify_timeslots_read', args=(self.event1.id,)))
        jsonstring = str(response.content, encoding='utf8')
        json = ast.literal_eval(jsonstring)
        self.assertEqual(expected_json, json)

    def test_modify_timeslots_update(self):
        """
        Test the POST response of modify timeslots from json file and change database.
        """
        thirty_mins = datetime.timedelta(minutes=30)
        time_range_start = datetime.datetime(2018, 2, 10, 2, 0, 0, 0)
        time_range_end = datetime.datetime(2018, 2, 10, 6, 0, 0, 0)
        deadline = datetime.datetime(2018, 1, 1, 0, 0, 0, 0)
        self.event1 = Events.objects.create(event_name="testEvent",
                                            time_range_start=time_range_start,
                                            time_range_end=time_range_end,
                                            deadline=deadline,
                                            duration=thirty_mins*2)
        self.timeslot1 = TimeSlots.objects.create(event=self.event1,
                                                  user=self.organizer,
                                                  time_slot_start=datetime.datetime(2018, 2, 10, 2, 0, 0, 0))
        self.timeslot2 = TimeSlots.objects.create(event=self.event1,
                                                  user=self.organizer,
                                                  time_slot_start=datetime.datetime(2018, 2, 10, 2, 30, 0, 0))
        self.timeslot2 = TimeSlots.objects.create(event=self.event1,
                                                  user=self.organizer,
                                                  time_slot_start=datetime.datetime(2018, 2, 10, 3, 0, 0, 0))
        modified_json = {"2018-02-10 02:00:00": "Blank",
                         "2018-02-10 02:30:00": "Selected",
                         "2018-02-10 03:00:00": "Selected",
                         "2018-02-10 03:30:00": "Blank",
                         "2018-02-10 04:00:00": "Blank",
                         "2018-02-10 04:30:00": "Blank",
                         "2018-02-10 05:00:00": "Blank",
                         "2018-02-10 05:30:00": "Selected",}
        response = self.client.post(reverse('manage_event:modify_timeslots_update', args=(self.event1.id,)),
                                    json.dumps(modified_json), content_type="application/json")
        event_timeslots = TimeSlots.objects.filter(event=self.event1, user=self.organizer)
        self.event1.refresh_from_db()
        q = TimeSlots.objects.filter(event=self.event1, user=self.organizer)
        d = []
        for Q in q:
            d.append(Q.time_slot_start.strftime('%Y-%m-%d %H:%M:%S'))
        for key, value in modified_json.items():
            if value == "Selected":
                self.assertIn(key, d)
            if value == "Blank":
                self.assertNotIn(key, d)

    def test_create_event_get(self):
        """
        Test the GET response of view create event
        :return:
        """
        response = self.client.get(reverse('manage_event:create_event'))
        self.assertEqual(response.status_code, 200)


class CreateEventViewTests(TestCase):
    """
    Test cases for create events.
    """
    def setUp(self):
        """
            Setup time_delta, time_now, max_time_range for manipulating data, then set up a valid form data.
        """
        self.organizer = User.objects.create(username="organizer",
                                             email="organizer@test.com")
        self.organizer.set_password('12345')
        self.organizer.save()

        self.client = Client()
        login = self.client.login(username='organizer', password='12345')
        self.assertTrue(login)

        self.time_delta = datetime.timedelta(hours=1)
        self.time_now = datetime.datetime.now()

        self.data = {'event_name': 'shadow',
                     'time_range_start': self.time_now + 2 * self.time_delta,
                     'time_range_end': self.time_now + 4 * self.time_delta,
                     'duration': self.time_delta,
                     'deadline': self.time_now + self.time_delta,
                     'info': ''}
