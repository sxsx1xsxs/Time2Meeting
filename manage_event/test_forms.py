from django.test import TestCase
from .models import Events, TimeSlots, EventUser
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.test import Client
from .views import *


class FormsTestCase(TestCase):
    def test_event_form(self):
        return