from django import forms
from django.test import TestCase
import datetime
from .forms import EventForm


class EventFormTestCase(TestCase):
    """
    This module is for testing forms.py
    """
    def setUp(self):
        """
           Setup time_delta, time_now, max_time_range for manipulating data,
           then set up a valid form data.
        """
        self.time_delta = datetime.timedelta(hours=1)
        self.time_now = datetime.datetime.now()
        self.max_time_range = datetime.timedelta(days=7)

        self.data = {'event_name': 'shadow',
                     'time_range_start': self.time_now + 2 * self.time_delta,
                     'time_range_end': self.time_now + 4 * self.time_delta,
                     'duration': self.time_delta,
                     'deadline': self.time_now + self.time_delta,
                     'info': ''}

    def test_clean_with_duration_greater_than_time_range(self):
        """
            clean() raises error 'duration error' for form whose duration is
            greater than time range while time range is positive.
        """
        new_data = self.data
        new_data['duration'] = new_data['time_range_end'] - new_data['time_range_start'] + self.time_delta
        form = EventForm(new_data)

        self.assertFalse(form.is_valid())
        with self.assertRaises(forms.ValidationError) as context:
            form.clean()
        exception = context.exception
        self.assertEqual(exception.error_list[0].code, 'duration error')

    def test_clean_with_time_range_end_earlier_than_or_equal_to_time_range_start(self):
        """
            clean() raises error 'end error' for form whose time range end is earlier than
            or equal to time range start.
        """
        new_data1 = self.data
        new_data1['time_range_end'] = new_data1['time_range_start'] - self.time_delta
        form1 = EventForm(new_data1)

        new_data2 = self.data
        new_data2['time_range_end'] = new_data2['time_range_start']
        form2 = EventForm(new_data1)

        self.assertFalse(form1.is_valid())
        with self.assertRaises(forms.ValidationError) as context1:
            form1.clean()
        exception1 = context1.exception
        self.assertEqual(exception1.error_list[0].code, 'end error')

        self.assertFalse(form2.is_valid())
        with self.assertRaises(forms.ValidationError) as context2:
            form2.clean()
        exception2 = context2.exception
        self.assertEqual(exception2.error_list[0].code, 'end error')

    def test_clean_with_time_range_start_earlier_than_or_equal_to_deadline(self):
        """
            clean() raises error 'start error' for form whose time range start
            is earlier than or equal to deadline.
        """
        new_data1 = self.data
        new_data1['time_range_start'] = new_data1['deadline'] - self.time_delta
        form1 = EventForm(new_data1)

        new_data2 = self.data
        new_data2['time_range_end'] = new_data2['deadline']
        form2 = EventForm(new_data2)

        self.assertFalse(form1.is_valid())
        with self.assertRaises(forms.ValidationError) as context1:
            form1.clean()
        exception1 = context1.exception
        self.assertEqual(exception1.error_list[0].code, 'start error')

        self.assertFalse(form2.is_valid())
        with self.assertRaises(forms.ValidationError) as context2:
            form2.clean()
        exception2 = context2.exception
        self.assertEqual(exception2.error_list[0].code, 'start error')

    def test_clean_with_deadline_earlier_than_or_equal_to_now(self):
        """
            clean() raises error 'deadline error' for form whose deadline
            is earlier than or equal to now.
        """
        new_data1 = self.data
        new_data1['deadline'] = self.time_now - self.time_delta
        form1 = EventForm(new_data1)

        new_data2 = self.data
        new_data2['deadline'] = self.time_now
        form2 = EventForm(new_data2)

        self.assertFalse(form1.is_valid())
        with self.assertRaises(forms.ValidationError) as context1:
            form1.clean()
        exception1 = context1.exception
        self.assertEqual(exception1.error_list[0].code, 'deadline error')

        self.assertFalse(form2.is_valid())
        with self.assertRaises(forms.ValidationError) as context2:
            form2.clean()
        exception2 = context2.exception
        self.assertEqual(exception2.error_list[0].code, 'deadline error')

    def test_clean_with_time_range_greater_than_max_time_range(self):
        """
            clean() raises error 'time range error' for form whose time range
            is greater than max time range.
        """
        new_data = self.data
        new_data['time_range_end'] = new_data['time_range_start'] + self.max_time_range + self.time_delta
        form = EventForm(new_data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(forms.ValidationError) as context:
            form.clean()
        exception = context.exception
        self.assertEqual(exception.error_list[0].code, 'time range error')
