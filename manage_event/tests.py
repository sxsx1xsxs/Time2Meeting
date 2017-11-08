from django.test import TestCase


from .models import Events, Users, EventUser, TimeSlots
# Create your tests here.

user_data = {
    'user_email': 'shadow.lzd@gmail.com',
    'user_name': 'Zhidong Liu'
}

event_data = {
    'event_name': 'shadow',
    'time_range_start': '2017-10-01',
    'time_range_end': '2017-10-08',
    'deadline': '2017-10-01',
    'duration': '30'
}


class EventsModelTests(TestCase):
    def test_was_published_recently_with_future_events(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_ = Events(pub_date=time)
        self.assertIs(future_events.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

