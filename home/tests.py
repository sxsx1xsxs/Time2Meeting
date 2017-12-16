from django.test import TestCase
from .views import *
from django.test import Client
from django.urls import reverse

class viewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get(reverse('home:homepage', args=()))
        self.assertEqual(response.status_code, 200)

    def test_team(self):
        response = self.client.get(reverse('home:team', args=()))
        self.assertEqual(response.status_code, 200)

    def test_guidance(self):
        response = self.client.get(reverse('home:guidance', args=()))
        self.assertEqual(response.status_code, 200)
