from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime


# Create your models here.
class Users(models.Model):
    user_email = models.EmailField(max_length=254, primary_key=True, blank=False)
    user_name = models.CharField(max_length=300)

    def __str__(self):
        return self.user_name

    def clean(self):
        if self.user_email == '':
            raise ValidationError('email cannot be blank.')


class Events(models.Model):
    event_name = models.CharField(max_length=300, blank=False)
    create_time = models.DateTimeField(default=timezone.now)
    time_range_start = models.DateTimeField()
    time_range_end = models.DateTimeField()
    final_time_start = models.DateTimeField(null=True, blank=True)
    final_time_end = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField()
    duration = models.DurationField()

    # record the status of the event, "Available' or 'Abort'
    status = models.CharField(max_length=10, default='Available')

    def clean(self):
        if self.time_range_start < timezone.now():
            raise ValidationError('invalid time range start point')
        if self.time_range_end < self.time_range_start:
            raise ValidationError('invalid time range')
        if self.deadline > self.time_range_start:
            raise ValidationError('invalid deadline')
    info = models.TextField(null=True)

    def __str__(self):
        return self.event_name


class EventUser(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(Users)

    class Meta:
        unique_together = ("event", "user")

    role = models.CharField(max_length=1)

    def test_


class TimeSlots(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(Users)

    class Meta:
        unique_together = ("event", "user")

    time_slot_start = models.DateTimeField()
